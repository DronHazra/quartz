---
title: CDS 2
tags:
 - exercises
 - uni
---

> Draw the resource allocation graph for the threads
> 
> A. `{ lock(m); lock(n) ; ++a; unlock(m); unlock(n); }`
> 
> B. `{ lock(n); ++a; unlock(n); lock(m); --a; unlock(m); }`
> 
> C. `{ lock(n); ++a; lock(m); ++a; unlock(n); unlock(m); }`

This can deadlock. Consider:
 - A locks `m` and C locks `n`
 - A waits for `n`, C waits for `m`, nothing ever makes progress

Since B never holds a resource while waiting, it doesn't have inward edges. 

> Emulate a mutex using asynchronous message passing

The simplest idea would be to have a process $M$ that is dedicated to maintaining the mutex. 

From the perspective of another process `p`:
 - locking:
	 - send a message to $M$ saying `p` requests a lock
	 - wait (sleep? `await`?) for a reply granting the lock
 - unlocking:
	 - send a message to $M$ saying `p` is releasing the lock

From the perspective of $M$:
 - consume message
	 - if lock request:
		 - am i locked? if yes, add `p` to my waiting queue.
		 - if no, reply granting the lock and lock myself (set internal state that i am locked by `p`)
	 - if unlock request (by `p`):
		 - if `p` is not the holder of the lock, send an error reply.
		 - otherwise,
		 - if my queue isn't empty, send a lock-granted message to the first process in the queue and update my state accordingly
		 - if my queue is empty, set myself to unlocked.

I wonder if you can do this with just 2 processes that communicate with each other, instead of having a dedicated lock manager. 

## a lock-free hash table
we already know how to implement a lock-free linked list, so if we use open hashing then we have a lock-free hash table for free, because your `insert`/`delete`/`get` operations are all operations on one of your linked lists. 

so you hash your key (which doesn't interfere with other threads), this tells you which linked list to perform the relevant operation on, and you perform the operation (append, delete, get) on that lock-free. 