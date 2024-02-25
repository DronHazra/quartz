---
title: "zilliqa intern post"
tags: 
 - SSE
---
I’ve been interning at Zilliqa this summer, and I’ve been working on some cool things I’d like to share!

  

I’ve been working on PDT — the Persistence Data Transformer. Zilliqa has a lot of data on the blockchain, stored as key/value stores in some S3 buckets. This is called “persistence” and has a record of basically everything that has happened on chain. We can’t really query this data to get anything useful out of it, but we’d like to be able to do that! Getting useful statistics like transaction throughput, keep track of events and token transfers, ask questions like “who owns this NFT” or “what volume has this account traded” and other things both users and developers might want to know. 
  

To make this happen we have to:

1. Download the persistence data
    
2. Transform it so it works with our database providers (BigQuery and Postgres)
    
3. Load it into the database
    
4. Extract some useful information out of it. 
    


It’s not quite that easy though. Persistence archives are really big. Obviously. And each one of these steps involves sending things over the network; networks can fail or reconnect and it would be really annoying if we had to restart from the beginning every time. So we’ve built each of these things (extract, transform, load) to be incremental — if the program crashes or we lose connection, we can start where we left off.

Another consequence of having our work being network-bound is that we'll be waiting for the network a lot. So we want everything to run concurrently so our cpu can get used while we’re waiting for the network.

My work was mostly working on steps 3 and 4, with a bit of 2. When i joined, we already had (1) working, and we had an implementation that imported everything into BigQuery courtesy of Richard Watts of the CTO. 

Let’s go over how it works!

1. Spin up N “threads” (really `tokio` tasks, but for our purposes they’re threads.)
2. As each thread:
	1. Find the starting point for my next batch of blocks
	2. Collect the microblocks and the associated transactions into their own vectors
	3. Take each vector, split it up so that our requests don’t trip bigquery’s size limit 
	4. Serialize into json and send it to BigQuery
	5. Tell BigQuery we’ve imported this batch of blocks
	6. Repeat!

We’ll get much more into Rust concurrency stuff later… because it's a joy to work with. Here we forget about most of it and just focus on making sure our threads don't step on each other's toes. We do this by pre-assigning them which ranges they’ll work on. 

Let’s say we have a batch size of 100 blocks, and 5 threads. then we’ll divvy up our range of blocks into batches of 100 and thread $i$ will handle every $i$-th batch. 

$$\{[0, 100), [200, 300), \dots\}$$

$$\{[100, 200), [300, 400), \dots\}$$

$$\{[0, 200), [300, 400), [500, 600)\}$$

  

[diagram]

  

this ensures no thread is stepping on another thread’s toes, and that we don’t have any missed blocks.

  

of course, if our program crashes, we have no guarantees about the state of our threads relative to each other — for all we know, thread 2 might have hit a range with a lot of transactions and gotten stuck while the other 4 threads raced ahead of it. say for example we run the program, and for whatever reason the user closes their laptop lid (i definitely didn’t do this). they first ran it with a batch size of 100, and when they restarted they decided to change the batch size to 200. that would mean this leftover batch

  

[diagram]

  

isn’t a full batch! we need a mechanism for keeping track of which thread got to where, and how to restart, and how to avoid duplicates. so, for each table we’re working with we’ll also have a “meta” table that’ll track what block ranges have been imported so far. whenever we import a set of blocks/transactions, we tell the meta table, and that way if we restart we’ll know what’s already been imported.

  

[footnote: you might notice that this doesn’t solve the issue of the program crashing in between importing data and committing to the meta table. this is pretty rare, but we also have logic in our insertion code to check whether there’s been any action in this range before we charge in and insert a bunch of duplicates.]

  

of course, implementing a meta table of this sort is profoundly annoying in an append-only system like bigquery. richard has some (well-documented and explained) magic that makes it work that i don’t pretend to understand:) but that’s how our bigquery implementation works, my first job was to take this and adapt it into postgres.

  

perhaps some personal information is due. before working at zilliqa, i had deleted more rust code than i’d written (i.e. i deleted the default code from a new cargo project and nothing more). but i appreciate the confidence (and patience!) my mentors richard and james had in me, throwing me into the pdt codebase written entirely in rust and answering my many, many, many questions. 

my first piece of work was taking apart the codebase and refactoring all the functionality i wanted across both backends into a shared library. this was a really good introduction to rust’s type system


```Rust
pub fn txns<'a>(
	&'a self,
	key: &ProtoMicroBlockKey,
	mb: &'a ProtoMicroBlock,
) -> Result<Box<dyn Iterator<Item = (H256, Option<ProtoTransactionWithReceipt>)> + 'a>> {
	let blk_id = key.epochnum;
	Ok(Box::new(mb.tranhashes.iter().map(move |x| {
		let hash = H256::from_slice(&x);
		if let Ok(maybe_txn) = self.db.get_tx_body(blk_id, hash) {
			(hash, maybe_txn)
		} else {
			(hash, None)
		}
	})))
}
```  

[about 2 weeks in i finally understood what these types meant!]  
  

having appropriately specified how i wanted the system to behave, it was time to actually implement this for postgres. i chose sqlx as the crate to talk to postgres because it seemed much easier to do things async. 

  

i won’t go through everything that had to happen, just the cool parts:) 

  

in bigquery, a lot of the database management things are handled for us (for ex, table partitioning is just a setting). you don’t have to worry about locking or indices or partitioning, just send requests and it’ll handle it for you. in postgres, you do have to worry about it.

for example, here's a problem that came up. two threads both get to the same new partition. the relevant partition doesn't exist, so both threads try to create it using "CREATE IF NOT EXISTS". except one of the threads errors out and skips the batch. but a priori we should expect that "CREATE IF NOT EXISTS" is just a no-op if the table is already created...

the problem is that "CREATE IF NOT EXISTS" isn't atomic. two concurrent "CREATE IF NOT EXISTS" commands can cause a race condition where one request checks the catalog to see whether the table exists *before* the other updates the catalog. this results in the second request aborting! (thankfully we know, at least!) so we have to set up some explicit locks. we do this using `pg_advisory_lock`, taking out a lock on the partition start. we also lump together our creation operations into one database transaction in sqlx, so that the lock is automatically released at the end of the transaction. 

another one of the cooler problems i had to work through was how to insert into postgres in a generic way. 

the most complicated part of our ingestion logic was managing tracking and concurrency, like we talked about before. so we decided to make that code generic over the actual items being inserted into them. this was fine for bigquery, since all we need to do there is serialize the rust struct into json. it's not so simple for postgres! sqlx doesn't like you inserting rust structs into postgres tables (check this), and it *especially* doesn't like you inserting arbitrary structs into arbitrary tables. 

this was a fun one. here's how my process went:

1. hmm, maybe we can just serialize into json, and convert from json into table rows?
2. can't do that without knowing the type beforehand, so let me serialize into json and *deserialize* into a hashmap and iterate over the keys to get each row
3. ok but now postgres thinks every field is json, and i can't cast the types without knowing the types

richard at this point suggested maybe using a macro! i'd heard of the concept of macros before (in this thing called... lisp) but i'd never used them before. and i have to say — macros are *so cool*. rust has two kinds of macros — declarative and procedural. declaratives are some
