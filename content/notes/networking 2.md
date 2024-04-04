---
title: networking 2
tags:
- uni
- exercises
---

## exercise 1
> Provide five examples of resource-multiplexing in computer networks. In each case state the layer of the network stack where this takes place, which resource is multiplexed and the multiplexing mechanism.

1. Multiplexing the physical link via frequency-division multiplexing. This is in the physical layer, it multiplexes the underlying physical link (e.g. optical fiber), and it does this by assigning each user a frequency range to transmit in.
2. In the link layer, MAC protocols are a form of multiplexing on the shared medium. It multiplexes the shared medium (e.g. the airspace of WiFi) by providing mechanisms to handle and avoid collisions that would otherwise prevent multiple users to use the medium. Depending on the protocol, the method of multiplexing is different — for example CSMA/CD is statistical multiplexing since it uses *random* exponential backoff. 
3. In the network layer, packets and packet buffers are used to multiplex network bandwidth. When the underlying link is full, the router stores packets in a buffer until there is link capacity available. This is statistical multiplexing.
4. In the transport layer, TCP multiplexes the underlying network interface by using port numbers and sockets. This uses a form of statistical multiplexing, with buffers and interleaving streams of packets being loaded into the network interface. 
5. In the application layer, a web browser/application might multiplex network traffic through an existing set of TCP connections. (I can't come up with another convincing case of multiplexing)

> Consider two clusters A and B each hosting multiple applications. All applications send bursty traffic between A and B over a link E. Under what conditions is circuit switching more efficient to use as opposed to packet switching?

Since the traffic is bursty, circuit switching is probably never *more* efficient. This is because circuit switching incurs an overhead for circuit reservation, so bursty traffic means lots of time spent setting up and tearing down circuits. If one considers efficiency as network utilization, packet switching will maximize throughput at times of high load while circuit switching will still only accept one application's traffic at a time. At lower load circuit switching incurs a higher overhead. As long as the packet headers are not massive, the setup and teardown of circuits outweighs the packet overheads. 

## exercise 2

> University of Whisky is about to open a new School with three new departments A, B and C. The IPv4 address prefix of the new School is 128.232.1.0/24 and it is expecting each department to have the following number of hosts:
> - Department A: between 40 and 60 hosts  
> - Department B: between 100 and 120 hosts 
> - Department C: between 20 and 30 hosts

> The university wishes to allocate a subnet for each department. Give possible IPv4 subnet masks for each new department.

Department A needs 6 bits, Department B needs 7, and Department C needs 5. 

So we can say: 
- Department B: 128.232.1.0/25 (`0|000_0000`)
- Department A: 128.232.1.128/26 (since 128=`10|00_0000`)
- Department C: 128.232.1.192/27 (since 192=`110|0_0000`)
where the `|` indicates the end of the subnet mask.

> Later, the School opens a fourth department D with 30 hosts. Provide possible IPv4 subnet masks to accommodate all four departments.

Same as before, but with Department D taking 128.232.1.224/27 (`111|0_0000`).

> Finally, the School opens a fifth department E of similar size to B. Provide possible IPv4 subnet masks to accommodate all five departments.

This isn't possible? Since we have total 256 IP addresses to allocate, and even in the minimum case we have 290 hosts?

## exercise 3

> The design of IP makes explicit provision for fragmentation, i.e. the ability to split an individual packet into pieces during its journey across the network. By considering the hourglass model, suggest why this feature is essential.

Without it, applications built on top of IP would have to know about the maximum size of packet that could be transmitted via the intermediate links in the network. That breaks the encapsulation IP is meant to provide. Since the internet has a wide variance in link capacity, fragmentation is necessary to ensure that different networks can interoperate and connect.

## exercise 4

> Explain how Ethernet performs carrier sense, collision detection, how it aims to minimise the probability of collision on retransmission and how this is adapted to handle varying load.

(Modern gigabit Ethernet is no longer multipoint, since all the connections are point-to-point and full duplex, so they don't need multiple access protocols anymore.)

Carrier sense: I check if there are any other messages being transmitted on the network and wait for the network to be clear before transmitting.

Collision detection: While transmitting, I listen for any other transmissions. If I hear anything, I have *detected* a collision, I abort my transmission and send a collision (jam) signal.

Minimizing retry collisions: I then wait for a random amount of time before retrying, and if we collide again I expand the range with which I can randomly choose from (binary exponential backoff).

## exercise 5
> Explain, giving an example, how to write a binary message (i.e. a sequence of binary digits) as a polynomial.

Counting from the right, take bit $n$ and encode it as the coefficient for $x^n$ of the polynomial.  

> Outline send and receive procedures for CRC-based message coding and error detection. What information must be agreed in advance by the sender and receiver?

Consider an $n$-bit CRC. The sender and the receiver have to agree on an $n+1$-bit number $p$.

Message coding of message $x$: 
- Find remainder $r = 2^n \cdot x \mod p$.
- Send $2^n \cdot x + r$ as the CRC message.

Error detection of CRC $x'$:
- Find remainder $x' \mod p$. 
	- If it is 0, no errors.
	- If it is nonzero, there are errors. 

## exercise 6

> - Explain in outline what is meant by a class of IP addresses. 
> - What problem did class-based addressing suffer?
> - Suggest one modification to the IPv4 class system which relieves this problem without moving to classless routing

A class of IP addresses has a dedicated prefix to indicate their class, and then a fixed number of bits to address the network, and the remaining bits to address hosts. This means that, for example, a Class A address (with leading bit 0, 8 bits to identify the network and the remaining bits to identify a host) is a class of addresses with few networks but many hosts per network — good for large ISPs. 

The problem with class-based addressing is that it allocates addresses in too-large blocks — a network too big for Class B would have to jump to Class A, getting 256x more addresses which they might not use all of. This means that each network might have a large number of addresses not in use. 

A small modification might be to remove Class A addresses, instead requiring a large network to have many subnetwork address blocks allocated as class B network. 