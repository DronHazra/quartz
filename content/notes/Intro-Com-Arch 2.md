---
title: Intro-Com-Arch 2
tags:
 - exercises
 - uni
---

## lecture 5 
> How does the RISC-V ISA make it easy to decode the source registers and why is this important?

In RISC-V, the source registers are always encoded in the same bits of the instruction, which makes instruction decoding very simple. This means that fetching the values from the register file can happen as soon as the instruction arrives (even if the values aren't needed) — fetching from registers can happen in parallel to the other instruction decoding steps (ex. decoding immediates). 
> How many addressing modes does the RISC-V ISA support and what are they?  

> Why is it reasonable to form immediates from many fields of the machine code instruction?

It offers some benefits including:
 - the source and destination registers are always in same bits
 - all the instructions can be the same length — there are less instructions with large immediates because they have less funct bits
 - decoding immediates ultimately comes down to shifting bits around, which is very fast in hardware

## lecture 6
> What is the difference between the data-path and the control-path, and why do they tend to flow together down the pipeline?

The data path is the path that the actual data being operated on travels through, whereas the control path controls which data to use and what to do to it. Since hardware is physical, the data path is *fixed* — we read both source registers every time, even if we don't need them. The control path are how the signals from the instruction and other state control how the data path correctly does what we want. 
> What is the difference between the following hazards: structural, data and control?

A structural hazard comes from some resource outside the processor core (ex. memory) that means that pipelines have to stall waiting for it. A data hazard is when an instruction depends on a previous instruction for its operands, while a control hazard is when an instruction depends on a previous instruction for its control signal. 
> What is code scheduling and how can it avoid stalls?

We can reschedule instructions so that more stages of the pipeline can be executed in parallel, avoiding stalls. An example is load hoisting, where we load values from memory as early as possible to avoid the instructions that use those values having to stall waiting for the load. 

## lecture 7

> How are forwarding paths used in processor pipelines? What pipeline hazards can they mitigate and what are the limitations of the mitigations?

Forwarding paths are used so that the results from a pipelining stage of one instruction can be directly used in a stage of the next instruction immediately, without.

They can mitigate data hazards by allowing a dependent instruction to fetch and decode instructions and fetch the other operands from the registers without having to wait for the previous instruction — the execute stage will automatically use the other dependent operand. They can also help with control hazards, where we can start fetching the relevant instruction as soon as we figure out where to go (at instruction decoding for unconditional jumps, or after execution for branches).

> Do pipelines always have five stages?

No, pipelines can have many different sizes for different architectures/microarchitectures

> For a pipelined processor implementing the RISC-V instruction set, why might branches cause bubbles in the pipeline, why are they needed and what can be done to mitigate them?

Branches can cause bubbles because the instruction fetch of the next instruction can't be run until the branch instruction completes. That means that the entire pipeline has to stall to wait for the one branch instruction. We can fix this with forwarding, mentioned earlier — except we forward which instruction to fetch rather than any data input/output. 

> What is branch prediction and how might it be used to avoid control hazards?  

We predict which branch we'll need to execute before we actually check — this lets us start executing the stages of the next instruction immediately.


## lecture 8
> What is cache miss rate and why must it be very low if it is not to have a major impact on processor performance?

The cache miss rate is the percentage of memory loads that actually have to query main memory. Querying main memory is very slow (on the order of 200 clock cycles for a fast processor core). So we ideally want almost every memory access to hit a cache instead of main DRAM. If cache miss rate is a little too high, then the entire processor core will slow down as it waits for memory accesses to complete. It's important to note that instructions are also stored in memory, so a high cache miss rate also affects the rate at which instructions are fetched and executed.

> Why do we need a hierarchy of memories rather than one big memory?

One big memory wouldn't be able to fit into a small area nearby the processor core, so the memory will be physically far away, and it'll take time for signals to arrive. Also, a larger memory takes longer to query to get values out of. So — we want a hierarchy of differently sized memories so that we get a balance of speed of access and capacity. 

> What are the principles of data locality exploited by caches?

Temporal and spatial locality — if we got a value recently, we'll probably use it again in the near future, and if we get a value in a location, we'll probably need nearby memory locations too. 

> What is the difference between: direct-mapped, set-associative and fully-associative caches?

Direct-mapped caches have a dedicated spot for every cache line, whereas a fully-associative cache 

> What are the differences between write-through and write-back policies?

Write-through means that copies of data in larger caches are also modified on write to the smaller cache, whereas write-back only writes it back when it is about to be replaced from the small cache. 

> What cache-line replacement policies are possible for direct-mapped and set-associative caches?

In a direct-mapped cache there is no choice. In a set-associative, there is a fully associative set of caches that each individually are direct-mapped. 

 - LRU: choose the one unused for the longest time. Simple for small numbers of entries, but hard to do this for to many.
 - Not last used: just check if an entry was the last one access and avoid evicting that
 - Random: doesn't have any pathological failures! and is easy to implement.
