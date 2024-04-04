---
title: networking 1
tags: 
- uni
- exercises
---
(dh700)

## exercise 1
 - a node is a person
 - the channel is the airspace of the room
 - not quite sure what an entity is
 - layer (assuming this means layers of abstraction) includes:
	 - physical production and transmission of sound via vocal cords + air
	 - body language and physical location layered on top of that
	 - the actual words being spoken
	 - the thoughts that are trying to be expressed
 - transmission is speaking
 - coding is the brain interpreting text and producing sounds via the vocal cords that correspond to language
 - addressing is done via body language and physical location — you indicate who you're talking to by where you are and where you're facing
	 - importantly, there isn't a general way of *locating* anyone in this room other than walking around
	 - one could imagine a host/organizer that keeps track of where everyone is, and this would let this approximation of addressing be closer
 - multiplexing is done both by physical location (the sounds you produce can roughly speaking only be heard within a certain radius) and also by the particularities of someone's vocal cords (someone's voice is identifiable and tells you who to listen to amongst other conversations you hear)

## exercise 2

**abstraction without layering:** instead of having different layers, another way we can get abstraction is via a standard set of messages following certain formats.  

**layering without embedding:** virtual machines work on top of real machines, but themselves offer all the facilities of a real machine that then gets chunked up and sent to real machines to do the work. 

## exercise 3
*frequency division multiplexing* and *time division multiplexing* are both ways of sharing a physical channel. FDM does this by splitting up the channel into various frequency bins and allocating these bins to different users. TDM does the same thing but on the time axis instead, splitting up the time axis into different frames, and further dividing those into slots within frames. Any given slot position in a frame is allocated to a single user/conversation. 

Frequency division multiplexing is harder to implement, both in terms of hardware complexity (transmitting signals at different frequencies) and also in terms of actually dividing it up. Frequency bands might be close together, and this could cause interference in deployment. 

## exercise 4
- what kind of traffic is suited to *synchronous time-division multiplexing*?
	- traffic that flows at a ~constant rate (since it will not leave its slots empty, reducing idle time)
	- traffic that requires latency guarantees (since data will be sent at certain times)
- define the term *circuit*
	- a *circuit* (in the networking sense) is a path through the network `A -> B` that is reserved for a certain node (here `A`) to use
- give an example of a circuit which is not implemented using time-division multiplexing
	- a circuit only requires that we reserve a path through the network, so it does not require use of time-division multiplexing. we can thus simply replace TDM with FDM, where reserving a circuit involves reserving frequency bands on each link.

## exercise 5
> Explain why *contention policies* are inherently more complex on a *shared media link* than a *point-to-point link* using *asynchronous TDM*. Give an example of each.

The fundamental challenge with a shared media link is that messages intended for one recipient are still sent to everyone — everyone else can hear what you're saying! This can lead to *collisions*, where multiple senders send a message and they interfere with each other. Also, on a shared media link, you may not be in range of every other host ("hidden terminals" problem), so collision avoidance and protocols that rely on knowing the whole state of the network don't work without modification.

A contention policy for a point-to-point link is having buffers when there is contention. For a shared media link, we have MAC protocols like CSMA.


## exercise 6
> The telephone network is an example of a *reservation* system. Explain what is happening when a caller dials a telephone number. Give two reasons why the delay between dialing a number and being connected (i.e. hearing the remote ringer) is variable.

When a caller dials a telephone number, the telephone system figures out an available path from them to the destination number in the telephone network and then reserves that circuit for their use. The length of time this takes could be variable due to:
- Variable distance between caller and callee — fundamental physical latency is higher/lower
- Variable overall network load — there may not be very many circuits available, and so caller might have to wait for a circuit to become available

