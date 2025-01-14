---
title: Multi-Protocol Label Switching
tags:
  - uni
  - notes
aliases:
  - MPLS
---
high-level: MPLS is a way to speed up forwarding for IP packets within a particular domain. it does this by *labelling packets on ingress* (with a fixed-length header) and then forwarding them according to their label until they exit the MPLS domain. there are various reasons to do this, including:
- speeding up IP packet forwarding
- moving routing logic into the data plane
- implementing differentiated service / policy routing
- fast failure restoration
- encoding "alternate routes"

some of them these are design goals of MPLS, and some of them are somewhat incidental. 

## how MPLS works
MPLS is a *shim* between the link and network layers. it can work with any protocol above or below it, hence multi-protocol. 

### MPLS headers
it has its own 32-bit header that it inserts between the network and link headers. this header has:
- 20 bits for the *label*
- 3 experimental bits
- 1 bit for the *stack*
- 8 bits for the TTL (to avoid routing loops)
the label defines a [[Forwarding Equivalence Class]]. ![[notes/Forwarding Equivalence Class|Forwarding Equivalence Class]]
### MPLS operation
- at ingress, compute the MPLS header and insert it into the packet
- at each [[notes/Label-Switched Router|LSR]]:
	- use the label to index into a forwarding table that specifies:
		- the next hop, and
		- the new label to attach to the packet
	- replace the old label with the new label and forward the packet
- at egress, get rid of the MPLS header and forward the packet based on IP/whatever else

the above description doesn't specify how to decide or communicate the forwarding information. there are two broad ways: hop-by-hop routes that query the dynamic routing protocol (ex [[Open Shortest Path First]]), or explicit routes where the whole path is set by the LSR.

>[!question] how is forwarding info decided? probably by the label distribution protocol? i don't know

keywords: frame relay — trade delay for optimal path
## downstream benefits and uses
MPLS labels can be used with differentiated service, letting you provide QoS. this is because you can configure LSPs between each ingress/egress pair, so by either using the `exp` bits or by creating an LSP for each traffic class you can implement differentiated service in that bit of the network. this decouples the number of traffic-class-paths from the number of flows by using MPLS' labels, so it scales better. it also still interoperates with the DS field-based architecture (what is this?). 

MPLS also enables fast failure restoration. specifically, we can get efficient *local protection*, where you keep around a backup path (and reserve resources, according to your SLA) for every possible link/node failure. the router that detects the failure will switch traffic to the backup router. this restores faster than end-to-end protection, since you can restore in the middle of the path rather than restarting from the source router. 

## rough notes
* instead of using ip masks for forwarding (longest prefix match), you circumvent the problem entirely  
* try to get at source routing via mpls  
* concept: use small, fixed-length field, so can decide forwarding just by indexing (fast in hardware)  
* adding a thin layer between link and network layer  
	* “shim”  
	* this is where “multi-protocol” comes in — you don't necessarily have to use IP on top or something?  
* this basically lets you do some routing *in the data plane*  
* MPLS headers have 32 bits  
	* 20 bits for label
	* 3 bits for “stuff” (experimental)  
	* stack..? (1 bit)
	* TTL (since you still want to avoid loops)  
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

