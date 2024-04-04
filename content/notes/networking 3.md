---
title: networking 3
tags:
- uni
- exercises
---

## exercise 1

> Consider a wireless network. For each of the following cases, state whether the packet transmission would be successful; assume no collision avoidance.
> - Nodes A and B are in range of each other; no other node is within range. Node A sends a packet to B.
> - Nodes A and B are in range of each other; nodes B and C are in range of each other; A and C are not in range of each other. Both A and C send a packet to B simultaneously.
> - Nodes A and B are in range of each other; nodes B and C are in range of each other; A and C are not in range of each other. C is transmitting and A wants to send a packet to B.
> - Nodes A and B are in range of each other; nodes B and C are in range of each other; A and C are not in range of each other. A is transmitting and B wants to send a packet to C.

1. Yes
2. No — the two signals would overlap and collide at B.
3. Yes — A would have heard B's CTS and deferred until it heard the ACK before sending its own RTS.
4. No — wireless connections are not full duplex, so B would not be able to send the packet. 

## exercise 2

> - What is the difference between routing and forwarding?
> - Routing algorithms can be either link-state or distance-vector. Define these two terms and explain the trade-offs between them.

Routing controls where packets should go to get to their destinations. Forwarding is the process that allows this — it takes individual packets and sends along their next hop. 

Link-state routing: every node knows about the links to its neighbours and their costs. Send your link state to all your neighbours, and whenever you receive a link state message, forward it to all your neighbours except the source. What this allows is every router to have the global network topology, and then each router can use Dijkstra and figure out the shortest path. 

Distance-vector routing: every node has a provisional shortest path length to every destination in the network (the titular distance vector). At regular intervals it shares this information, and receives its neighbours' distance vectors. Each node then updates its own shortest paths based on the options provided by its neighbours. 

Link-state takes a lot of messages to set up, and computing Dijkstra is expensive, and link states can be big, but it's less likely to cause loops between nodes. This is because every node has (up to network reliability) a global picture of network topology. Distance-vector is more efficient, with each node keeping only the distance vector and iteratively converging on shortest paths rather than flooding and then computing. However, this eventual convergence makes it more vulnerable to having loops. In particular, in LS each node computes its own table, while in DV the "table" is distributed among all nodes, so DV lets errors propagate throughout the network.

## exercise 3

> You are required to design a topology discovery protocol for a network of switching nodes interconnected by links. There are n nodes, l links, the maximum degree of any node is k and there is a path between any two nodes of not more than d hops. All links are bi-directional.
> 
> Each node has a unique identifier of four bytes which it knows.
> - (a) Describe a protocol for a node to learn about its immediate neighbours. You should specify the format of your messages and the size of any message fields.
> - (b) Using the characteristics of the network described above, design a protocol for distributing this information across the network. You should specify the format of your messages and the size of any message fields.

Let's go with the simplest protocol. The only message we'll need is "I am node `[id]`, I am your neighbour." In a message format, the only field we'll need is the source node id. 

```python
# maintain which node is on which link
# this also doubles as our node set
link_map: map[link, node] = {}

def on_receive_message(node, link):
	# when we receive a message, add them to our neighbours
	link_map[link] = node

start_message_handler(on_receive_message)

for link in links:
	send(self.id, link)
```

Basically what we do here is that we tell all our neighbours who we are. If every node does this, by symmetry every node will know all of its neighbours. We assume a node can decide what link to send to, and what link a message is coming from.

To distribute this information is a little trickier. I'll use something similar to eager broadcast. 

Add another message that says "Nodes `a` and `b` are neighbours." We don't explicitly indicate the source here, since forwarding a message unchanged is likely faster than processing and then forwarding. This also requires some information in the message to indicate what type of message we're sending. So our two messages are something like:
```
Discover:
- Message type (1 byte)
- Node id (4 bytes)

Update:
- Message type (1 byte)
- Node id 1 (4 bytes)
- Node id 2 (4 bytes)
```

Message type could just be 1 bit, but because of alignment it wouldn't make a difference anyway — and this gives more flexibility for future message formats. 

```python
link_map: map[link, node] = {}
network_state: map[node, set[node]] = {}
def on_receive_discover(node, link):
	link_map[link] = node
	# update our part of the network topology
	network_state[self.id].add(node)
	network_state[node].add(self.id)
	
	for outgoing_link in links:
		# tell everyone about this update
		# notably including the original sender, so they know who we are
		send(update(self.id, node), outgoing_link)

def on_receive_update(node1, node2, link):
	# forward the update to everyone but the sender
	for outgoing_link in links:
		if outgoing_link != link:
			send(update(node1, node2), outgoing_link)
	# update our own network state
	network_state[node1].add(node2)
	network_state[node2].add(node1)

start_message_handlers(on_receive_discover, on_receive_update)

for link in links:
	send(discover(self.id), link)
```

## exercise 4
> Following are some examples of routing strategies and real systems which use them. For each one, suggest one reason why the strategy is a good choice, and another in which it might cause problems:
- (a) flood routing in an Ethernet hub  
	- (flood routing is when you forward every message you receive to everyone but the sender)
	- it might be good, since an Ethernet hub has high capacity and flood routing has very low processing complexity, so it can be fast and cheap,
	- but it isn't very efficient
- (b) random routing in a peer-to-peer file-sharing network 
	- (random routing is when you forward every message to a random link?)
	- a P2P network has very high churn, so the robustness of random routing is helpful in a quickly changing environment
	- but it's obviously inefficient, and if you need a particular file (that's too many hops away) you may not be able to get there in a reasonable amount of time.
- (c) source routing in the road network
	- (source routing is deciding a path ahead of time and then following it)
	- it makes forwarding very easy, since every packet has the full path indicated
	- but it's vulnerable to link failure, since the router cannot dynamically go around blockages during transit (like a road closure, for instance)

## exercise 5

> (a) Consider a subnet with prefix 192.168.56.128/26. Give an example of one IP address that can be assigned to this network.

192.168.56.129 (trivially, it matches the first 26 bits)

> (b) Suppose an ISP owns the block of addresses of the form 192.168.56.32/26. Suppose it wants to create 4 subnets from this block, with each block having the same number of IP addresses. What are the prefixes (of form a.b.c.d/x) for the four subnets?

192.168.56.`00|10_0000` is the ISP mask, so the 4 subnets are:
- 192.168.56.0/28 (`0000|_0000`)
- 192.168.56.16/28 (`0001|_0000`)
- 192.168.56.32/28 (`0010|_0000`)
- 192.168.56.48/28 (`0011|_0000`)

The strange part is the fact that the ISP block has a `1` in the host bits? I don't really know how to deal with that.

