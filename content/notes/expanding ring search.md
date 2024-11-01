---
title: expanding ring search
tags:
  - definition
---
This is essentially iterative deepening search: you search for something within a certain "distance" of yourself, and and then you expand your search area incrementally. This lets you avoid wasting resources by searching too broadly in the beginning.

This has applications in broadcast protocols, since you want to avoid wasting network resources by searching too widely. It is easily implemented using [[notes/multicast routing|multicast routing]], sending messages with a certain TTL to limit your search radius. This can do automatic load balancing too, since heavily loaded servers will drop packets and so won't respond. 

> [!example]
> discovering a printer on a local network — you want to search locally first