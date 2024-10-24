---
title: networking 5
tags:
- uni
- exercises
---
## exercise 1

- How can websites keep track of users? Do they always need to use cookies?
	- They can also use their own login credential systems.
- Describe how Web caching can reduce the delay in receiving a requested object. Will Web caching reduce the delay for all objects requested by a user or for only some of the objects? Why?
	- A copy of the requested object is kept in a network node closer to the user, which means that the round trip time to get the object is reduced.
	- It may not reduce the delay for all objects, since certain objects may not be available or up-to-date in the closer, cached instance.
- Under what circumstances is file downloading through P2P much faster than through a centralized client-server approach?
	- When a large number of people want different downloads, because the server caches aren't useful, but the load on the individual server is very high. A P2P network will distribute the work among many different hosts serving different files.
- Assume a BitTorrent tracker suddenly becomes unavailable. What are its consequences? Can files still be downloaded?
	- Yes, since each peer in the network can still revert back to the slow method of letting other peers know about what peers its connected to. 

## exercise 2
> Let’s see how you can troubleshoot the network!
> 
> A relative has contacted you for help; they believe the Internet is broken. The fault turns out to be that a piece of network-protection software had installed a specific IP address entry for an (alternative) default DNS server.
> - (a) What is DNS and why we need DNS for network system.
> - (b) What should have provided the correct DNS entry?
> - (c)By concentrating on how DNS is intended to work, describe why network applications may not work correctly
> - (d) How would you diagnose this problem?

DNS is a registry that maps domains to IP addresses. It's needed so that machines and websites can have human-readable names instead of just IP addresses. In particular, IP addresses might change and the DNS will handle that change and ensure the same domain continues working — this allows a layer of abstraction between applications and ISPs.

The local DNS server was supposed to provide the correct DNS entry.

It's possible that the alternative default DNS is giving incorrect answers or doesn't exist — this would explain why the internet isn't working. Without the translation from domain names to IP addresses, visiting a website won't work. To diagnose this, 

> Now the DNS server problem has been solved. But we soon found that the DNS server has been poisoned (sometimes this is referred to DNS hijacking).
> - (e) Outline how spyware might use an (alternative) DNS entry to attack the DNS server
> - (f) Describe a network-centric method for overcoming such treachery

Spyware might add a DNS entry that tells the DNS server to request a malicious server for certain domains, instead of the normal server. This would mean network traffic to a trusted website like google might get redirected to a malicious address.

We can stop this using DNSSEC, which signs the DNS responses using a chain of trust from the root server.

## exercise 3
> Assume you request a webpage consisting of 1 document and 5 images. The document size is 1 kbyte, all images have the same size of 50 kbytes. The download rate is 1 Mbps and the RTT is 100ms. How long does it take to obtain the whole webpage under the following conditions? (Assuming no DNS name query is needed and the impact of the request line and the headers in the HTTP messages is negligible)

- (a) Nonpersistent HTTP with serial connections
	- 1 RTT to establish a TCP connection,
	- 1 RTT to request the file,
	- each of these overheads are *per object*
	- `6 * 200 ms + 1 ms + 5 * 50 ms = 1451 ms`
- (b) Nonpersistent HTTP with 2 parallel connections
	- 1 RTT to establish TCP connection (100)
	- 1 RTT to request document (100)
	- 1 ms to get document
	- see 5 images, get 2 at a time:
		- 1 RTT for TCP
		- 1 RTT to request image
		- 50 ms to get image
		- 250 ms
	- 3 total batches needed, so
	- `201 ms + 3 * 250 ms = 951 ms`
- (c) Nonpersistent HTTP with 6 parallel connections
	- 1 RTT to establish TCP connection (100)
	- 1 RTT to request document (100)
	- 1 ms to get document
	- see 5 images, get 5 at a time:
		- 1 RTT for TCP
		- 1 RTT to request image
		- 50 ms to get image
		- 250 ms
	- `201 ms + 250 ms = 451 ms`
- (d) Persistent HTTP with 1 connection.
	- 1 RTT to establish TCP connection
	- 1 RTT to request document
	- 1 ms to get document
	- request 5 images (1 RTT)
	- 250 ms to download all images
	- `201 ms + 100 ms + 250 ms = 551 ms`

## exercise 4
> An older home-network router has an upload bandwidth of 1Mbit/s to the Internet, and a 100kbyte first-in first-out (FIFO) buffer for packets awaiting transmission. Packets have a maximum transmission unit (MTU) of 1500 bytes.


- If the buffer is completely full, how long does it take the router to transmit all of the bytes in the buffer?
	- 0.1 seconds
- Suppose the router supports two FIFO queues, one high-priority for interactive appli- cations (like Voice over IP) and the other lower-priority for all remaining traffic. If a VoIP packet arrives when the queue for interactive applications is empty, what is the maximum time before the router starts transmitting the VoIP packet? (Assume that the router does not preempt any ongoing packet transmission.)
	- `1500 bytes / 1 Mbit/s = 0.012 s` since the router might have just started sending a max-size packet.

## exercise 5

- Outline the advantages of IPv6 
	- Larger (=more) addresses
	- better security?
	- fragmentation only at the source => simpler middleboxes
- Does IPv6 eliminate the need for NAT?  
	- Yes, and no — IPv6 has many more addresses, which is one of the main problems NAT is used to solve. 
	- However, NAT is still very useful because it provides security properties within a network by, for example, preventing hosts within a network from being directly addressed.
- Is SLAAC really an advantage over DHCPv6?  
	- Once again, yes and no
	- Yes, because it's much simpler and faster, and doesn't require a dedicated server to be running DHCP,
	- but No, because it can cause privacy issues: in SLAAC hosts can be identified across networks, and MAC addresses are often embedded in the identifier used.
- Compress this ipv6 address: `2001:1a24:0000:0000:1b12:0000:0000:1a13`
	- `2001:1a24:0:0:1b12:0:0:1a13`
	- `2001:1a24::1b12::1a13`

## exercise 6
> Host A and B are communication over a TCP connection, and Host B has already received from A all bytes up through byte 126. Suppose Host A then sends 2 segments to Host B back-to-back. The first and second segments contain 80 and 40 bytes of data respectively. In the first segment, the sequence number is 127, the source port number is 302 and the destination port number is 80. Host B sends an acknowledgement whenever it receives a segment from Host A.

- In the second segment sent from Host A to B, what are the sequence number, source port number and destination port number?
	- 207, 302, 80
- If the first segment arrives before the second segment, in the ACK of the first arriving segment, what is the ACK number, the source port number and the destination port number?
	- 207, 80, 302
- If the second segment arrives before the first segment, in the ACK of the first arriving segment, what is the ACK number?
	- 127

> Suppose the 2 segments sent by A arrive in order at B. But the first ACK is lost and the second ACK arrives after the first timeout interval. Draw a timing diagram, showing these segments and all other segments and acknowledgements sent (assuming there is no additional packet loss). For each segment in your figure, provide the sequence number and the number of bytes of data; for each acknowledgement that you add, provide the acknowledgement number.

![[Pasted image 20240326173721.png]]