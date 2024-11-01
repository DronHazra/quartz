---
title: Border Gateway Protocol
aliases:
  - BGP
tags:
  - uni
  - notes
---

> [!info]
> The Border Gateway Protocol is the current widely-used protocol for *interdomain routing* (routing between Autonomous Systems (AS)). 

the first and foremost thing to understand about BGP is that it's a *mess*. lots of networking protocols are evolutionarily designed, with pieces added on and optimizations made based on the environment. they have some kind of defined protocol with a bunch of variations on how to implement it. BGP *is not like this.* it serves basically as the glue protocol for the internet, letting all the big ISPs talk to each other even though they might all be optimizing for different goals. as such, the relationships between various networks (which are negotiated by real people with real contracts) are by-and-large encoded in BGP attributes.

so it's worth spending some time setting up some conceptual infrastructure to understand what we might want out of an interdomain routing protocol. if you squint, it almost looks like a spec.  

## interdomain routing
*managing relationships between networks*
  
* ok…. so customers…… pay providers…. for access to the network….
* this is one kind of relationship
* we also have "peers" i.e. competition
	* and the peers can be easily changed (no lock in?)
	* we want to be able to flexibly change between providers by reconfiguring
* peering gives you connectivity too (bilateral incentive)
	* since you want your customers to reach customers of other providers and vice versa
* peers *don't provide transit* — if A peers with B peers with C, traffic from A to C won't be carried by B
	* because it doesn't match B's incentives — their network gets used, but no one is paying them to do that (since the end customers are A and C customers)
* but as with anything to do with human negotiation, exceptions abound
* peering is highly negotiated — business relationships between peers are secret
	* to peer?
		* you get lower transit costs, since both peers will have to less traffic with the provider above them
		* probably better end-to-end performance (since it reduces the path length)
		* and in the case of tier 1's, you might not have another way to reach them [^tier1]\
	* or not to peer?
		* wouldn't you rather just have a customer
		* peers are your competition, so you don't want to help them too much either
* we want to be *valley-free*: you can only traverse provider-customer and peer links
	* i.e. you follow customer-provider links up, travers peer links, and then provider-customer links down
	* you don't go up after going down
	* something something "well bracketed"

[^tier1]: NB: tier 1 ISPs have global connectivity, so in general the number of AS-es that you need to traverse is not very large, doesn't go much higher than around 6. most of routing is done within ASes

## the actual protocol bits
okkk lets actually talk about BGP
* BGP distributes *reachability* information, computing paths between AS’s (groups of IP network prefixes, network providers) 
* and what info you distribute lets you control policy
* BGP is a *vectoring* protocol, but not a distance vector one (path vector instead) to hack some of the problems out (namely loop avoidance)
* a BGP router distributes:  
	* what prefixes can be reached  
	* and how to get there, according to *me*  
* don’t flood info, send individual messages..?
* AS’s have a number
* AS graphs *hide information*
	* they do not represent the actual internet topology  
		* so e.g. you might choose a shorter *AS* path, but it might be longer if you look at the IP topology  
	* we tolerate this because otherwise it gets really messy 
		* the best route can change frequently, and there's a lot of routing state
		* so if the gateway protocol were to take the local routing into account, you might lose convergence properties
* you don’t *always* need to use BGP — you can just statically “nail up” your network with a default route to a particular ISP
	* this is *static routing*
	* it also forms the difference between an *autonomous routing domain* and an *autonomous system*
	* this is approximately what your home router does
	* these are expressed as "default" routes
* and in fact you can also technically have multiple ASes for a single ARD (since they have multiple AS numbers)

ok *now* let’s talk about BGP

* first you send your active routes
* and then when you receive info, you make some decision on what path vectors to share
* two parts: external (between different AS’s) and internal (multiple border routers in the same AS)

### internal BGP (iBGP)
* you need the internal version because:
	* you need to be able to see what ASes are reachable from your other border routers
	* and you need to know that you can reach your border routers directly
	* and the internal protocol for doing this needs to account for the fact that we're in a single AS
	* and you might have different policies at each gateway
* the internal version also has to work differently! consider a case where i have 3 border routers A, B and C
	* B tells A it can reach C
	* A re-tells B it can reach C
	* the link from B-C is removed: now A and B both think the other can reach C
	* this is the [[count to infinity problem]]
* eBGP avoids having to deal with this since it is a path vectoring protocol, so it distributes full paths with all the AS numbers (makes loop avoidance trivial)
* but iBGP is in the same AS! so that trick doesn't work
* what you have to do is say "i will not forward route information from internal peers"
* but then how can you guarantee that information from external peers gets distributed?
* you have to form a *mesh*
	* each iBGP router talks to each other
	* they advertise external peering info to all the internal peers
* aside: these iBGP things (meshes) don’t scale
	* cause every pair of internal BGP routers have their own BGP session, its a mesh  
	* so routing table is O(N) larger than number of best paths  
	* so fixing it?  
		* route reflectors — just passing on updates between IBGP *via* best routes, and have a group of internal routers that are allowed to re-advertise routes  
		* break an AS into multiple pieces and glob it together — confederation (make it look like a single AS)  
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
