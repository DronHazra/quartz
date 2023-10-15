---
title: "thoughts on software eng"
tags: 
 - SSE
---
> Because in that world, software is in fact "soft" - in a large complex real time control system like the Shuttle's avionics system, software is pervasive and, in virtually every case, the last subsystem to stabilize. Software by its nature is the easiest place to correct problems - hut by that very nature, it becomes a tyrant to its users ard a tenuous and murky unknown to the analysts. Software is the easiest to change .... but in change, it is the easiest to compromise.

from https://www5.in.tum.de/persons/huckle/space_.pdf

i always oscillate between the two modes of:
 - programming most things is so easy, how on earth are software engineers paid so much, this seems ripe for outsourcing/automation
 - programming is one of the hardest things humans can do, we are awful at it, software engineers should be paid more because we need to attract the best people — **it's a miracle this works at all.**

i think this quote succinctly articulates why software doesn't seem hard and actually is hard. 

building a bridge is hard because no bridge is ever exactly the same, and you need people to design the bridge with the appropriate principles so as to be safe, and then construct it such that it satisfies the necessary physics. except once you start building the bridge, you are building the bridge. the brige is being built. you can't very easily decide halfway through to change the building materials. and yet software is like that — enticingly flexible so as to make specifications seem unnecessary, and brutal in the impossibility of writing software with 0 errors.

software doesn't have physics lying underneath — the same protocol can be used for 2 or 2 trillion network packets, but that flexibility means it's hard(er) to test. 