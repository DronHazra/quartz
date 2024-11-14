---
title: You Can't Do Anything With A Packet
tags:
  - principle
---
In a high-speed network, the routers and switches have to process millions of packets per second, so any computation done per-packet very quickly blows up in practice. I first heard this kind of thing from my college academic advisor. About his time writing video codecs, he said "you can do whatever you want with a compressed video frame, duplicate it, reverse it, make it do a dance — but you can't do anything with an uncompressed frame."  

This reflects a really general engineering principle that tends to pop up across many software domains. Many systems have an inherent bottleneck that rudely remind us, constantly, of the futility of optimizing any other part of the system. 

- Switches/routers forward packets as fast as possible -> simple FIFO scheduling
- Training neural nets requires a bunch of FLOPs -> only worry about GPU util

There are other examples that feel less clean to explain. Processor cores are fast, but memory access is slow -> you can't do anything with memory (caching, locks). Cores are fast but context switches are slow -> you can't do anything with processes (concurrency). Computation is fast but consensus is slow -> you can't do anything you have to agree on (EVM gas fees, distributed state).

I appreciate this especially because it takes the opposite stance to most academic CS courses. Most CS courses are about things we *can* do, algorithms and techniques people have come up with and maybe even used. But not very many of these courses focus on *the constraints the system places on us.* We can be as clever as we want with scheduling algorithms, but the real network traffic will beat us into submission. 

> You can walk outside and listen to all kinds of talk, get told that you’re a god or a total bastard. The Iron will always kick you the real deal. [Iron and the Soul](https://www.oldtimestrongman.com/articles/the-iron-by-henry-rollins/#:~:text=You%20can%20walk%20outside%20and%20listen%20to%20all%20kinds%20of%20talk%2C%20get%20told%20that%20you%E2%80%99re%20a%20god%20or%20a%20total%20bastard.%20The%20Iron%20will%20always%20kick%20you%20the%20real%20deal.)

