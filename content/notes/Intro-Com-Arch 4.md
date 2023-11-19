---
title: Intro-Com-Arch 4
tags:
 - uni
 - exercises
---
## hardware sync primitives
> What sort of synchronisation primitives might an atomic fetch-and-add be useful for?

It would be useful for implementing mutexes and semaphores, which could be used as the basis for higher-level concurrency techniques like monitors.

> With load linked / store conditional, why does the store alter the source register containing the value to write?

It does this to indicate whether the store conditional has succeeded or failed.




