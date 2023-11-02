---
title: CDS 1
tags:
 - exercises
 - uni
---

## the bakery algorithm and hardware sync primitives
you start with two (global) arrays indexed by the thread id (`tid`) — `Enter` and `Number`.

conceptually — each thread enters the bakery, takes a numbered ticket, and then waits until all the lowered-numbered-tickets get cleared, and then the lock is acquired. once the thread is done with the critical section, it clears its ticket and leaves.

`Enter[t_i]` indicates whether `t_i` is currently entering the bakery. it's set to `true` when `lock` is called, and set to `false` once the thread has its ticket. once the thread has its ticket (which it stores in `Number[t_i]`), it iterates over all the threads, waiting for each thread `t_j`:
 - if thread `t_j` is currently getting a ticket, wait for them to finish getting the ticket
 - then if `t_j` has a lower (nonzero) ticket, or if it has the same ticket (this can happen since getting a ticket isn't mutex-guarded) but has a lower id, i.e.   `(Number[t_j], t_j) < (Number[t_i], t_i)`, wait for their ticket to be cleared
 - lock acquired!
releasing a lock just involves setting `Number[t_i] = 0`.

the key thing to notice here is the spinning! because we have no hardware sync primitives, we can't sleep waiting for a lock and then be woken up once the lock is available. 

## semaphores vs mutexes
a semaphore is a shared and bounded counter with atomic increment (`signal`) and decrement (`wait`) operations. these operations will only be completed once their result is within the bounds, otherwise they'll block waiting for the operation to be valid
 
a binary semaphore (only values of 1 or 0 are allowed) is, in essence, a mutex. take a semaphore `Locked` which is 1 if a thread holds the mutex, and 0 otherwise.  you `wait` to acquire a lock (`0->1`) and `signal` to release it (`1->0`). if the lock is already held when the call to `wait` is made (`Locked=1`), the thread blocks. 

a semaphore is more general than a mutex though, because we can manage concurrent access to N resources. instead of having an overlapping system of different locks for each instance of a resource and having each thread decide which resource to unlock, we can use a semaphore to handle availability of the entire set of resources. the semaphore also contains state inside it, so we can use it for condition synchronization across threads. 

> can you build a semaphore from a mutex?

a binary semaphore is equivalent to a mutex anyway. a larger semaphore definitely can't be expressed with just one mutex (it only contains one bit of information). even if you have N mutexes, you can't atomically get access to the state of all of them. also, N-resource semaphores don't usually provide mutual exclusion, since multiple threads might be in the relevant section of code. so a mutex would be more restrictive, would probably impose some order of resource allocation — seems impossible.

