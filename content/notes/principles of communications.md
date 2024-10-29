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
* BGP doesnt have a formal spec — so we’ll look at trying to define a formal spec  
* ok…. so customers…… pay providers…. for access to the network….  
* and bgp also encodes the fact that there are “peers” i.e. competition   
	* and the peers can be easily changed (no lock in?)  
* peering gives you connectivity too (bilateral incentive)  
* tier 1 providers: global connectivity   
	* this also means that AS-path-lengths are small — most of the routing happens locally rather than between ASes  
* BGP is (maybe?) valley-free: you can only traverse provider-customer and peer links (cant go the other way)  
* peering is highly negotiated — business relationships between peers are secret

okkk lets actually talk about BGP

  

* BGP distributes *reachability* information, computing paths between AS’s (IP network prefixes)  
* and what info you distribute lets you control policy  
* BGP is a *vectoring* protocol, but not a distance vector one (path vector instead) to hack some of the problems out  
* a BGP router distributes:  
	* what prefixes can be reached  
	* and how to get there, according to *me*  
* don’t flood info, send individual messages..?  
* AS’s have a number  
* AS graphs *hide information*  
	* they do not represent the actual internet topology  
		* so e.g. you might choose a shorter *AS* path, but that might be shorter if you look at the IP topology  
	* but we do this anyway because it gets really messy  
		* more instability in routes, large amount of routing state (might lose convergence properties)  
* you don’t *always* need to use BGP — you can just statically “nail up” your network with a default route to a particular ISP

ok *now* let’s talk about BGP

* first you send your active routes   
* and then when you receive info, you make some decision on what path vectors to share  
* two parts: external (between different AS’s) and internal (multiple border routers in the same AS)  
* aside: this iBGP things don’t scale  
	* cause every pair of internal BGP routers have their own BGP session, its a mesh  
	* so routing table is O(N) larger than number of best paths  
	* so fixing it?  
	* route reflectors — just passing on updates between IBGP *via* best routes  
	* break an AS into multiple pieces and glob it together — confederate (make it look like a single AS)  
* types of messages:  
	* open: establish a peering session  
	* keep alive: heartbeat/handshake  
	* notification: shuts down a peering session  
	* update  
* what do you send in the announcements:  
	* basically: the prefix, and some attributes  
	* AS\_PATH is the path to a particular AS, from me  
	* MULTI\_EXIT\_DISC:   

* how do you decide? in order:  
	* relationships: highest local pref  
	* traffic engineering:  
		* shortest ASPATH  
		* lowest MED (what is med? well im glad you asked, i dont know) (oh it’s MULTI\_EXIT\_DISC, the choice for which exit route to use)  
		* prefer external learning vs internal routes (to get traffice off your network as fast as possible)  
	* give up, just do a tiebreak:  
		* lowest router id

we have the general concept of control and data planes
* each layer in the network is the control plane for the data plane below  
	* e.g. a router has a switch in it
* when a route announcement crosses an AS boundary, we update the next hop info  
* and we have to connect up the internal routing with the external routing, by connecting up iBGP to eBGP

  

right so now the policy bits:

  

* how do you control customer/provider and peer/peer relationships?  

* you filter out the routes that you export and only advertise customer and ISP routes when you tell your provider and your peers  

	* this means you don’t transit other network’s traffic (no-valley routing)

  

hmm the correct way to discuss this is basically to talk about a bunch of attributes:

  

* AS PATH length — trivial  

* local preference in iBGP, lets you say (in essence) which border router to exit from (which might decide which AS you go via)  

* **![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXfUcujPDAEfPOFD1HIqlDEZhBE4uJjAOjX5XTyp-gc9yrMgfhK0fZzwnz6A2-fBHHfBAkt4jwqf87EJq7hv4NGk2iAClc6eTDjCGsy2vNP7GW4uwzQqAnfZeaRNjGrtjX9JxYym5C0BoXtVfPwzNCsWeFlJ?key=E3KfSIv_6lfmAhlBjZSwsQ)  

* ASPATH propagates as a list, which gives you loop prevention for free  

* (but traffic doesn’t need to follow the ASPATH\! it can, or it can not, yk, basically its this big coordination game)  

* and this is because the AS graph depends on your point of view because of information hiding — different players have different views of the game state  

* local preference is a good way to control your outbound traffic… but how do we do this for inbound traffic?  

* well… its a little dumb… but you can just let your “primary” inbound router have a short AS path length, and just artificially duplicate nodes in the AS path your backup router advertises  

* this doesn’t always work, because local preferences take precedence over ASPATH length  

  * so you can Call Human (do some negotiating) and then use the community attribute to do the path length  

* all of this is decided by human coordination/contracts/negotiating etc  

* MED \= multi exit discriminator: advertising internal distance to a certain prefix  

  * this can be used to make hot potato routing nicely  

  * make provider (high bandwidth backbone) carry the bits most of the way

  
