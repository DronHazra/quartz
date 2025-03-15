---
title: adv-comp-arch supervision 3
tags:
  - arch
  - uni
  - exercises
---
## multithreaded processors
coarse-grained: flush the pipelined instructions
fine-grained: in-order pipeline with interleaved instructions
SMT: out-of-order processor, like you have a wider issue window (separate functional units)
### VLIW processors and fine-grain multithreading
(a) (i) VLIW processors are Very Long Instruction Word processors, which accept batches of instructions that can are able to be executed in parallel. This guarantee is provided by the compiler — fine-grain multithreading lets the processor (and thus the compiler) care about fewer data/control hazards to pack the instructions.

(a) (ii) round-robin schedules are ineffecient because it schedules stalled threads

(a) (iii) meta: execute correctly = consider correctness. 

what changes to the processor do you need to make to allow an optimised thread scheduler to execute correctly? well you have to talk about all the extra hazards you introduce

(a) (iv) shrinking requirements down, better code density, don't have to conflict flops vs intops



### pairing threads in SMT
In pairing threads, we want to avoid choosing threads that are bottlenecked on the same resources. For example, we want to avoid pairing two threads that are both bottlenecked on  floating-point arithmetic. A good pairing might be a memory-bound thread with an execution-bound thread, since the execution-bound thread can get lots of core time while the memory-bound thread waits for its memory operations to execute. 

We also would like to avoid pairing threads that depend on each other in some way. This might be the case if two threads read and write to the same regions of memory. This introduces data hazards that limit the amount of instruction-level parallelism we can achieve. 

We might also want to pair threads that can gain performance by being executed simultaneously. For example, if two threads read from the same range of memory, the whole cache line will be fetched for both threads. This means that the performance of the threads will be higher than if they were executed serially. 

In summary, we'd consider:
- resource requirements/bottlenecks
- dependencies between threads
- synergistic performance impacts

notes:

not really any returns beyond 2 threads, sometimes you even turn off SMT with two threads

note: share a working set

further note: dont schedule threads that block on each other

### adding thread contexts vs cores
Adding more cores adds more execution capacity and decreases pressure on shared resources (L1 cache, TLB) but needs more power and chip area. For workloads that are bound by 

notes:

adding cores make them smaller (smaller caches, less functional units etc)

shared vs private caches and dynamic/fixed partitioning 

multicore = different issue window/frontend, SMT = duplicate 

fixed area budget roughly translates to fixed power budget (since you have roughly the same number of transistors)

## the memory hirerarchy
### large L1 caches and page sizes
If your page size is smaller, you likely have more pages, so you might need a larger TLB, which competes for core-local fast memory. 

VIPT—virtual indexed, physical taxed (synonyms)

### cache prefetching
you might be limited by the size of your caches, since looking too far ahead might cause you to overfill the cache/evict useful data. you also might evict the prefetched data before it gets used if you prefetch too much.

you might also be limited by your memory bandwidth, since you need to be able to get the prefetched data from memory into your caches

as with caches, your workload might not satisfy your assumptions of spatial/temporal locality, so fetching more cache lines is just wasted effort

### L3 cache compute
basically long-reuse timers or like dispatch instructions 

## vector processors
precise exceptions impose an in-order constraint