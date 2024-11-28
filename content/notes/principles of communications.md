---
title: principles of communications
tags:
  - uni
  - notes
---
MPLS:

  

* instead of using ip masks for forwarding (longest prefix match), you circumvent the problem entirely  
* try to get at source routing via mpls  
* concept: use small, fixed-length field, so can decide forwarding just by indexing (fast in hardware)  
* adding a thin layer between link and network layer  
	* “shim”  
	* this is where “multi-protocol” comes in  
* this basically lets you do some routing *in the data plane*  
* 32-bit header:  
	* 20 bits for label
	* 3 bits for “stuff” (experimental)  
	* stack..?  
	* TTL (still want to avoid loops)  
* build a label-indexed forwarding table  
* i.e. *label switching router*  
* forwarding a packet involves more complexity than just “straight on through”  
* often you want some extra information? in the forwarding? some tying between network and link layers  
* “differentiated service” or something  
* and this is complex and annoying to do on every hop  
* and so MPLS lets you sort sets of packets that are all treated the same by an label-switched router (forwarding equivalence classes)  
	* i.e. when you enter the MPLS network (*ingress*), you decide all this stuff *once*, include that info in the label, and then you can do all your policy stuff fast in hardware with simple label lookup

ok so how does this work  

* packet enters the mpls domain  
* you stick in the shim (i.e. encode the packet’s forwarding equivalence class into the label)  
* these labels have local significance (cause 20 bits is too little to be unique)  
* so the switching operation is now:  
	* (interface in, input label, interface out, label out) entries in table  
	* forward packet to interface out, and map label in \-\> out  
* something something label distribution?  
	* what does this do i have no idea  
* ok now how do you *decide* these routes within the MPLS network  
	* can query the routing protocol at each hop: *tell me the next hop*  
	* or you can do explicit routing  
	
		* i.e. at ingress, the control protocol sets the route that should be used  
		
		* so you can deal with “other information” (policy, differentiated service, etc etc)  
		
		* protocols: CR-LDP, RSVP-TE

ok so why isnt this used everywhere


* what happens when things break?  
* state is *installed* somehow, these forwarding tables are state, what happens if the state changes  
	* switch breaks, how do you reroute when you do source routing?  
* this is kind of fine when the paths are dynamically installed by routing protocols, but harder when you do end-system-installed routes  
* IP restoration you need to wait for the routing protocols to update with protocols  
* MPLS also gives you fast failure restoration  
	* you also set up a backup path in advance  
	* link- and node-disjoint with the main path  
	* but this needs fast notification of failure  
		* aside on failure detection  
			  * its nontrivial to do this  
			  * but actually you get this implicitly in the PHY  
	* the amount of resources you dedicate to do this restoration is defined by the SLA  
* right so this needs “local protection” which means you need to distinguish backup paths  
	* so *this* is what the stack is for

an aside on segment routing

* fast failover part of MPLS (move traffic from segment of path to other segment)  
* operates at IP layer (so it doesnt give you any forwarding benefits really)  
* so something of a specification of things you want  
	* policy  
	* active segment  
	* push  
	* next  
	* continue  
* source routing in IPv4 is usually blocked for DDoS reasons (not authenticated)

ok now a somewhat bigger picture: thus far we’ve been talking about distributed routing (LS \+ disjskstara) and centralized (fibbing and SDN), now we’ll talk about federated routing

* federated routing connects systems that autonomously routing within themselves (network of networks)  
	* concept: cant optimize for particular metrics cause local networks optimize for different things  
	* so we basically optimize for reachability  
* so we’ll talk about BGP, which manages relationships between networks  


[[notes/Border Gateway Protocol]]




[[notes/multicast routing]]

[[telephone routing]]

[[flow control]]

## scheduling
the overview here is basically "what if we didn't just do first-come-first-served scheduling." in doing so, we'll have to talk about what we want out of a scheduler, how good schedulers can be, and where they can be used. 

scheduling in a network is basically a simpler version of OS scheduling, since you have many fewer resources to manage. there are a couple unique things about packet scheduling that make the tradeoffs play out differently ([[notes/You Can't Do Anything With A Packet|You Can't Do Anything With A Packet]]). 
### requirements of a scheduler
- ease of implementation
	- [[You Can't Do Anything With A Packet]]
- performance bounds
- fairness (and relatedly, protection)
	- [[notes/max-min fairness|max-min fairness]]
	- protect flows from other misbehaving flows (avoid one flow taking more than its "fair share")

there are various ways to vary a schedules:
- how many priority levels?
- work-conserving? [[work-conserving scheduler]]
	- work-conserving schedules get more utilization, potentially at the cost of jitter/instability in servicing time
- how granular are your service levels?
	- per application? user? end-system?
- how do you service individual queues?

the simplest scheduler is 

so we talked about scheduling in routing, and the main reason that you do anything fancier that first come first served is to get "fairness." the main model we use is [[max-min fairness]]

the model to use here is [[Generalized Processor Sharing]]. in general, the broader internet doesn't (or can't) implement this kind of thing.

one way to attempt this is just a [[Weighted Round Robin]] (weighted fair queueing? nvm it's not WFQ) . it's easy to implement, but:
- mean packet sizes can differ between flows (e.g. audio vs video traffic)
- mean packet sizes can *vary* (think compression)
- some flows might only be visited once (short-lived flows)

so we can help the packet size issue by using [[Deficit Round Robin]]

[[Weighted Fair Queuing]]

## datacenter networks

problem: synchronization messages (`memcached`, Naiad, other things) get slowed down by high throughput (e.g. data), and so the whole distributed algorithm runs slower.

so we can implement [[QJump]]

code lives in the hypervisor system

qjump doesn't scale beyond modest size datacenters

## a perspective on optimization as network protocols

routing:
- fixing the paths, how do you set the rates?
- fixing the rates, how do you choose traffic paths?
- where do you set the path rates?
	- centrally
	- at endpoints (distributed algo)
	- routers

objectives?
- minimize system-wide delay with
	- variable: routing 
	- fixed: source-destination traffic rates
	- you have a bunch of flows that are sending data at certain rates (between a source and a destination)
	- and you vary the paths that you send the traffic along
- maximize system-wide utility with
	- variable: traffic rates
	- fixed: paths
	- each source chooses the rates they'll send at, and we want to maximize the overall system utility
	- notably: can't centralize this easily, since you can't know everyone's utility fns
	- "billing" view
- constraints:
	- capacity constraints


ok basically there's this cool way of thinking about TCP congestion control as "a distributed asynchronous algorithm" to solve this problem — reflects the evolutionary nature


so in the congestion control model, we can do "bidding" on the bandwidth, and you can coordinate this with the network with pricing (congestion charging) $$x_s = \frac{w_s} {p_s},$$ so basically "i'm willing to pay this much" is the $w_s$, network says "i'm charging you this much per unit bandwidth" $p_s$, and this means the bandwidth you *get* is $x_s$. 


## capacity planning

fill this in later, but roughly you measure things and reallocate capacity

## system design in networking
resources to manage:
- time
- space
	- metcalfe's law: net value is square of number of nodes
		- network effects, i.e. if each new user brings resources with them the value goes up by n even though marginal cost is 1
		- 
	- networks can often "scale out"
	- self scaling = added cost costs less than resource gained
	- efficiencies of scale
- computation
- energy
- money
- labour
	- fiber rollout in the uk: 2008 crisis => recession => cheap labour => lots of fiber rollout
- education/skills

