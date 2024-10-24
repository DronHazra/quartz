---
title: Intro-Com-Arch 1
tags:
 - uni
 - exercises
---
## lecture 2
> why is timing analysis so important and how is it used to determine critical paths and the maximum clock frequency?

the goal of timing analysis is to determine, for a given configuration of FFs and gates and wires and a physical layout (including a clock frequency), whether the FF setup and hold times are satisfied, and ensuring the clock doesn't skew beyond the boundaries that would prevent us from having digital time.

critical paths are used by timing analysis — these are paths that bottleneck how fast a processor can be clocked. a critical path is the longest path a signal could take to determine the eventual circuit output. the clock frequency must allow enough time for a signal to propagate through the longest critical path and still satisfy the setup and hold times for the FFs as well as having the correct circuit output during the relevant clock cycle. essentially — we want the outputs of a circuit to change with the clock edge, and so the signal needs to make it through the longest path.

timing analysis is especially important since the processor manufacturer is liable if the timing analysis turns out to be inaccurate; without correct timing analysis the maximum clock frequency might cause the chip to make mistakes/errors at the gate level — very bad!

> what steps are involved in compiling a SystemVerilog design into an FPGA image?

![[Pasted image 20231029195558.png]]

1. the SystemVerilog design is compiled into a directed graph of gates and wires in the "synthesis" stage. the word "compiled" here is important, since this process can involve varying degrees of optimization, like boolean optimization (reducing number of gates) and placing an input function before an FF instead of after in order to relax timing constraints ("retiming").
2. we define some constraints like chip size/area, clock speed and other timing constraints, i/o pin locations, and we put these into an optimization process that figures out where to put all the components and wires — this is "place and route" .
3. from here we have enough to make an FPGA image! we can also do gate-level simulation and timing analysis to verify the clock speed is safe, and if not, we have to go back to place and route to retry with a slower 

> why is synchronization important for correct operation of a clocked digital circuit?

you can't control when asynchronous inputs will change, but these changes can violate setup/hold time requirements for FFs and cause metastability, which can cause undefined behaviour since it violates the digital abstraction of 1s and 0s. we want to be able to respond to asynchronous inputs without having it violate our neatly arranged digital clock abstraction, and so we need to use synchronization. 

(briefly, synchronization is using two additional FFs hooked up to asynchronous inputs such that even if the first FF goes metastable, the synchronized input isn't affected until the second FF also updates. this gives the first FF time to resolve. resolving from metastability is a probabilistic process, but we can design systems to control the MTBF (mean time between failure))

## lecture 3

### how to do computer architecture

**1. design for moore's law**
   processor designs need to be updated to keep up with moore's law, but chips are expensive to produce and costly to get wrong. consider adopting a tick tock update cycle, where you alternate between either upgrading the architecture or the silicon. even now, when the silicon itself isn't getting much faster, designs still need to focus on how best to use the increasing transistor density (which is still growing exponentially). 
**3. use abstraction to simplify design**
   fairly self-explanatory: just as we use abstractions in software for reliability, testing, and collaboration, we want to use abstraction for hardware as well. 
**4. make the common case fast**
   a 10x increase in performance for an instruction used 1% of the time is only a 0.9% overall improvement — but it might require you to clock your processor a little bit slower, and this is a performance hit that every instruction in the other 99% has to take. focus on commonly used instructions and make these fast. 
**5. to gain performance — parallelize**
   hardware is inherently parallel, so a lot of performance can be gained by doing more things in parallel. one way to do this is instruction-level parallelism on superscalar processor cores, where multiple instructions are executed at once. we can also do instruction lookahead, where we look at the next N instructions and figure out what can be executed in parallel. this also plays into pipelining. 
   we can also take advantage of different cores! thread-level parallelism. for example, having the operating system run on its own dedicated core so that the other cores can run threads without as many context switches, or using dedicated custom chips optimized for things like video decoding.
   lastly we can have data-level parallelism with vector instructions — perform operations on vectors of operands. this is used especially in GPUs. 
**6. to gain performance — pipeline**
   loading instructions or operands from memory can take many cycles to complete. we don't want these cycles to be spent idly, so instead we should split instructions into steps and interleave their execution so we can better utilize our processing power.
**7. to gain performance — predict**
   since hardware is inherently parallel, it's often better to try to execute something both ways and throw away the result if its not needed or incorrect. an example — backwards branches tend to be taken much more often, since a lot of code involves loops. so we might then guess that the backwards branch will be taken and then deal with the consequences later. other assumptions, like assuming data is "probably the same" or assuming that data recently accessed is needed soon can yield big speedups. 
**8. use a hierarchy of memories**
   accessing DRAM could take 300+ clock cycles. signals take a long time to travel relative to the speed at which modern processors are clocked. this is the von neumann bottleneck, but having a hierarchy of memories/caches — where small+fast memories are placed closed to the processor core and caches get successively larger and slower as we go down the hierarchy — can help alleviate this because of locality assumptions.
**9. get dependability with redundancy**
   error correcting codes mean we can keep some redundant bits around and this allows us to guarantee correctness even at certain levels of failures. this can also mask certain hardware defects. this is a tradeoff though — for example, flash storage typically have very sophisticated error correcting mechanisms because they favour capacity over reliability, .

## lecture 4

RISC — reduced instruction set computer. the risc-v philosophy is that ISAs should be open-source and standardized to allow for more portability, and that each instruction does minimal work, as opposed to the "complex" instructions of other CISC systems. risc also wants to be an easier target for compilers, since more of the internal operations are exposed to the compiler (because the instructions themselves do minimal work).

> is RISC-V a processor?

RISC-V isn't a processor, it's an instruction set architecture. 

> what is the difference between a pseudo instruction and a conventional one?

a pseudo instruction might get translated to multiple instructions when actually run, whereas a conventional instruction will always be just one instruction. otherwise, if the instruction length is the same, a pseudo instruction is just an alias for the underlying conventional instruction, usually with specific arguments baked in.

> why are there many more R-type instructions than U-type instructions?

R-type instructions have extra `funct` bits that, in a U-type instruction, are taken up by the immediate. 

> what is a load-store architecture?

a load-store architecture is one where arithmetic/logical operations are only computed on registers, not on values in memory. values from memory have to be loaded into a register first.

