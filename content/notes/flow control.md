---
title: flow control
tags:
  - uni
  - notes
---
- you have to match the send capacity to the receiving capacity
- so what do you want out of flow control?
- overhead
	- want to actually send packets, not just figure out the correct rate to send
- scaling
	- networks are getting bigger and faster! esp datacenter network
- fairness
- "stable"
- tradeoffs between all the above!

normally flow control is handled by tcp/quic/transport layer (i.e. as an end-to-end system). you can't have flow control in IP, for some reason, but you can have flow control in datalink layers too (esp in shared media layer, where we call it "contention control" (collisions!))

- forward reference to control theory! 
	- source -> ($\lambda$) buffer/bottleneck? -> $\mu$ -> sink (round trip) -> source
	- this is abstract, but on any link you'll have *some* bottleneck so its not too bad a model 


ok! now a taxonomy

- open loop
	- no continuous feedback loop
	- "can i have this?" "no" "bye"
	- operation?
		- call setup, then transmit data
		- network defines parameters
		- user chooses parameter values they need
		- network says yes or no
	- notably the network has to police the usage
- closed loop
	- feedback loop
	- source monitors what available service rate is
		- explicitly or implicitly! e.g. lack of acks
	- like a steam engine!
	- there's a bunch of choices: 
		- how complicated is it to compute? how accurate do you want to be? how do these scale?
		- ex on a very very large network link (like 400 gbit/s) 
- "hybrid"


a couple things to think about here:
- how do you describe what flow you need?
	- a phone call is *fixed* in terms of bandwidth demand
	- e.g. the star wars title card is quite hard to compress
		- video compression is variable rate — so a single object can have many data rates when you're streaming it!
- want descriptors to be:
	- representative
	- verifiable
	- preservable (closed under network transformations)
	- useable..?
- for ex!
- time series of interarrival times (sequence of timestamps)
	- not very useful, but *very* representative!
- peak rate
	- verifiable, preservable, useable, but not representative!
	- useful to guarantee capacity
- average rate
	- if you can sustain long buffering, this is ok
	- could do moving windows, or jumping  bounds
- [[linear bounded arrival process]]
	- because you have buffers! 
- note that, 
	- telephone call peak rate = average rate = constant across calls
	- so it was quite easy to do this


ok now closed loop systems
- vary rate by window size (remember tcp)/data rate 
- how do you get feedback?
	- explicit: network tells you directly
		- more control, but more overhead
	- implicit: end-to-end principle
		- observe based on outcomes
- window size is somewhat useful, can also control rate explicitly
	- need a timer
	- but finer-grained, so better control
	- more overhead  (because of timer interrupts, though you could implement this in a network card instead of at the os level)
	- (e.g. tcp cubic)
- normally in the internet we do end-to-end flow control,
	- but we can also do hop-by-hop! e.g. in space you might do tcp with each hop instead of end to end
- the benefit of end-to-end is that end hosts are usually much more powerful than routers, its cheaper etc

ok let's build up some flow control things (notably similar to )

- receiver can give on and off signals
	- e.g. a printer over a serial link (usb)
- stop and wait
- ECN (congestion notification) = DECbit
	- set bit based on how long queues are