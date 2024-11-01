---
title: multicast routing
tags:
  - notes
  - uni
---

- so you could have some block of ip addresses that are dedicated as "multicast address" [[Class D Addresses]]
- senders send to the address, and receivers request packets from that address
	- could lead to DDoS attacks since anyone can send to the address
- the magic is in associating the group address to all its recipients: a *dynamic directory service*
- Four problems  
	- which groups are currently active
	- how to express interest in joining a group
	- discovering the set of receivers in a group
	- delivering data to members of a group
- a simple application is [[expanding ring search]] which you can use for resource discovery

## implementing multicast
- there are different flavours of multicast
	- **unicast:** point to point
	- **single-source multicast:** point to multipoint
	- **any source multicast:** multipoint to multipoint
	- each of these can be simulated a set of the one above
		- point to multipoint = set of point to point unicasts
		- multipoint to multipoint = set of point to multipoint multicasts
	- but they vary in efficiency
- source copying (unicast)
	- i.e. source sends copy of packet to each destination
	- this is inefficient not just at the source node (because the source sends multiple messages), it's inefficient across the whole distribution tree from source to destination, since links carry duplicate packets
	- but it is efficient for number of groups set up, since each multicast group is just a collection of unicasts— no group overhead
- single-source multicast
	- 1 message sent from each source
- often, these days, last-hop networks have LAN broadcast, i.e. ethernet
- so maybe you can use ethernet to multicast, and translate "class D" addresses to ethernet addresses 
	- map in group ip address to broadcast ethernet address
	- nb ethernet networks are usually switched these days instead of on a broadcast medium, so the switches have to emulate the broadcast medium
- so we use [[reverse path forwarding]]
- er.... so we talked about a bunch of protocols which i truly don't understand so (TODO go over this)


- but as it turns out all of this sucks and doesn't work
	- multicast gives you *huge leverage* for spam and DDoS attacks
	- its source-controlled, anyone can send to groups
	- and not only that, creating new groups even with no recipients can cause a bunch of extra control info to be computed for routers
	- causing extra computation without any cost: bad
- so now we have the *application layer alternatives* to multicast
- like CDNs! e.g. akamai
- an aside on youtube
	- when you upload a video, it only keeps the copy on the nearest youtube server
	- if it *gets interest*, then youtube replicates the video to all the servers
	- this works because the source copy load is comparatively low (movies release slowly)
- an aside on netflix
	- have deals with ISPs to put netflix boxes in ISP sites
- can have caches either be demand filled (youtube) or pre-fetched (apple software updates)
- i.e. youtube pushes data to youtube servers, managed networking