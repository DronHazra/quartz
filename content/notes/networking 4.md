---
title: networking 4
tags:
- uni
- exercises
---

## exercise 1
> What can an enterprise do to prevent their competitors to infer the path or topology inside themselves by using traceroute while keeping the normal ping between the source and destination working.

An enterprise can simply not send back the ICMP control message when the TTL expires on an IP packet inside their own network (or at their gateway). This would allow normal traffic through (like `ping`) but would stop `traceroute` from inferring the pathway. 

Alternatively, they might simply send the ICMP message that tells traceroute it's found the destination at the gateway itself. 

## exercise 2
> Consider the test network below; Y and Z are two unix IPv4 hosts, while nodes A through E represent fully-conformant IPv4 routers providing the only connectivity between the two hosts.
> ![[Pasted image 20240324182529.png]]
> Per-packet load balancing by A and E means packets may be sent on any valid path. No firewalls or packet filtering is used anywhere in the network.
> 
> Using traceroute infers the following paths:
> - (Y-A-B-C-E-Z)
> - (Y-A-D-E-Z)  
> - (Y-A-B-D-E-Z)
> - (Y-A-B-E-E-Z)
> Explain (with diagrams as appropriate) why these results have occurred and identify the two true and two false results;

Staring with the more interesting ones, (Y-A-B-D-E-Z) occurred because B and D both responded to the traceroute probe, and so were both included in the traceroute output?

## exercise 3
 - **What is the difference between congestion control and flow control in TCP?**
	 - flow control ensures TCP doesn't overwhelm the receiver, congestion control works for the network as a whole. 
 - **Describe on-off flow control. In what circumstances is it appropriate?**
	 - on-off flow control is where the sender sends data until the receiver is full, waits for the receiver to empty its buffer and then starts again. it might be useful when traffic is bursty, because unlike tuning a sliding window size, the changes in transmission are immediate. 
 - **Describe the operation of window-based flow control**
	 - the receiver has a window size that indicates how many packets the sender is allowed to have in flight (this is the same window used in congestion control),
	 - this window size is based on how much buffer space is available on the receiver end. it's set such that the buffer will never overflow.
	 - the sender can send `window_size/RTT` packets per second, so the receiver will set the window size so that the buffer empties as fast or faster than packets arrive. 
 - What happens if a flow using window-based flow control passes through a highly-loaded switch or router? You may assume the switch or router does not participate in the flow control protocol.
	 - flow control does not care about network load!
	 - the packet might get dropped/delayed due to high load, but the receiver would then increase the window size saying "my buffers are emptying, i can take more packets"
	 - the sender would thus *increase* its transmission rate, and the load problem would get worse, more packets dropped, vicious cycle.
 - How is this addressed in the TCP protocol?
	 - congestion control! in TCP, increase the window size until a packet gets dropped, and then halve it (additive increase multiplicative decrease)
 - What are the advantages and disadvantages of having Internet routers participate in window-based flow control of every TCP connection?
	 - well flow control is definitely not in the domain of routers, it's a property of the end hosts, so routers would not provide any advantage
	 - for *congestion*, routers have the benefit of knowing the status of the network and its links and so might be able to advise TCP to reduce its window size before packets get dropped.
	 - but this also involves some mixing between layers, which breaks encapsulation
	 - and this also makes standardization harder — some TCP implementations might ignore IP-level congestion heuristics

## exercise 4
> Assume that three TCP flows $f_1$, $f_2$, $f_3$, share a single link. The bandwidth of the link is 200 Mbps. The desired bandwidth of each flow is: $f_1$ 60 Mbps, $f_2$ 80 Mbps, and $f_3$ 100 Mbps.
> 
> Answer the following questions:

- (i) What would be the max-min bandwidth allocation of the flows?
	- $f_1$: 60 Mbps, $f_2$: 70 Mbps, $f_3$: 70 Mbps
- (ii) Propose a way to “cheat” max-min fairness so that $f_3$ increases its allocated bandwidth as computed in Part (i).
	- Split the flow in 2 pieces, each of 50 Mbps. 200/4 = 50, and so both those flows are immediately satisfied, the net flow is 100 Mbps.

## exercise 5

- What is ARQ?
	- Automated Response Query — a class of protocols that provide error and loss detection and facility to retransmit when errors/loss occurs
- Describe and the design and operation of a simple ARQ for a lossy communication channel.
	- The sender adds some checksum bits (e.g. with CRC) to each message, along with a sequence number. 
	- On receipt of a message, the receiver checks the checksum. If it's fine, it sends an acknowledgement (ACK). If not, it sends a NAK. Both have the sequence number attached. If the receiver already received this message, it doesn't use the data. 
	- If the receiver gets a good ACK, they can continue sending. If they get a NAK, they retransmit. If they get something corrupted, they retransmit anyway. 
- When and why does a simple ARQ at the transport layer have a significant negative impact upon application performance?
	- If the RTT is high, then the application has to wait for a round trip for every packet sent, limiting throughput
- Describe what additions are required to a simple ARQ to support windowing. When and why will an ARQ which supports windowing provide better application performance than a simple ARQ?
	- We already have sequence numbers, we just need a way to set the window size. Otherwise, we can set up our ACKs so that they acknowledge *all* packets up to that point, and then when a packet is dropped or corrupted, we go-back-n and retransmit everything in the window.

## exercise 6
> Consider a scenario where Host A, Host B and Host C are connected as a ring.
> 
> Assume that Host A and Host C run protocol rdt3.0 while Host B simply relays all messagers received from Host A to Host C.
> - Does this arrangement enable reliable delivery of messages from Host A to Host C?
> - Can Host B tell if a certain message has been correctly received by host A?

It does enable reliable delivery of messages (under reasonable assumptions about the underlying links) — this is effectively TCP over IP/ethernet, where the lower layers get the packets to their end destinations. 

Host B *can* tell, since A's ACKs will go via B. 