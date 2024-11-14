---
title: Weighted Fair Queuing
tags:
  - definition
---

Simulate [[notes/Generalized Processor Sharing|GPS]] to figure out when a packet would be finished in the *ideal* case, and then serve packets in the order of the predicted finish times.

the problem is that now your scheduling algorithm depends on how busy your network is — when a flow finishes, you have to recompute everything, 