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
