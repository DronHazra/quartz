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

### spin locks
> Assuming a single instruction `xchg` that can do an atomic exchange of a register and memory location, how would you implement a naive spin lock?

```asm
lock: mov  r3, #1 // load 1 into r3
	  xchg r3, 0(r1) // swap 1 into *r1
	  bneq r3, lock  // if r3 is 0, the lock was free. otherwise,
	  // the lock was held and we should spin
```

> Instead of inefficient spinning on a lock, how might you alter the lock and unlock code from slide 27 to call routines wait for unlock and signal unlock to wait when the lock is already taken and signal other threads once the lock is free? Don’t worry about implementations of wait for unlock and signal unlock, but assume that when the former is called it returns once the lock is free and that the latter should be called after unlocking to tell all waiting threads that the lock is now free.

```asm
lock: mov  r3, #1
	  lr   r4, 0(r1)
	  bneq r4, wait_for_unlock
	  sc   r3, 0(r1)
	  beqz r3, lock
```

```asm
unlock: st zero, 0(r1)
		j signal_unlock
```

### memory barriers
> What does a memory barrier do?

It ensures that any memory operations written before the barrier complete, and any memory operations after the barrier must occur after the barrier. This is to prevent the typical optimizations done in hardware that reorder load/store instructions to improve efficiency. 

> Why do we place a memory barrier after taking a lock and before releasing the lock, but not the other way round (i.e. before taking and after releasing)?

Our goal with the memory barrier is to ensure that critical memory operations that are meant to occur when a lock is held *only occur when that lock is held*. To this end, we want to stop these operations from occurring before or during lock acquisition, so we need a memory barrier after taking the lock. We want to stop these operations from occurring after we've already released the lock, so we need a memory barrier before releasing the lock to ensure all those operations execute before we release the lock.

## GPUs
### SIMT
> Describe SIMT, one way GPUs exploit parallelism. Apart from performance, what are the other benefits of SIMT execution?

SIMT is Single Instruction Multiple Thread, where a single instruction will execute in multiple threads, each with their own registers, state and data. 

> How does the processor pipeline differ from a general-purpose CPU to allow SIMT execution?

First, each thread has its own stack and registers. The data is streamed to many many small cores, each with its own small ALU. Work is divided up into warps, which are collections of threads that run together. Second, because memory latency is high but we need to trawl through lots of data, we do multithreading on each core. When one warp stalls, we start running another warp to hide latency. 

The instructions are obviously shared between threads. Each thread executes the same instruction, greatly reducing the total latency for fetching instructions.

> What are the implications for other parts of the processor for providing SIMT (e.g. the data cache)?

The data cache might be implemented per core, with higher levels of caches shared between cores. The cache hit rate will be lower than typical CPUs since GPUs usually trawl through lots of data, and so data isn't commonly reused. We need a warp scheduler that decides which warp to run, and each core usually has multiple register files to handle switching between warps easily. 

### GPU efficiency

> What is the basic way GPUs allow branching within the different threads?

A thread only executes if a predicate is true. This reduces efficiency since each branch means you have less threads doing work at a time. 

You should write code for GPUs in such a way that avoids complex branching as much as possible to increase your utilization. For infrequently taken branches, you should aim to have as little work done as possible, since all the threads in the warp have to wait for the infrequently taken branch to complete before continuing.

> Assuming each line below is a single instruction, what is the efficiency of the code (ignoring predicate manipulation instructions)?
```
   ld X[i:i+3]
   if (i % 2 == 0)

     mul a, X[i:i+3]
   else

     mul b, X[i:i+3]
     if (i % 4 == 1)

       add c, X[i:i+3]

       mul 2, X[i:i+3]
     endif

endif
```

25%?

> Why do GPUs rely on parallelism between warps as well as SIMT? What bottleneck does this target?

The bottleneck here is memory latency — we don't want to wait for memory in order to do useful work. So while one warp is stalled waiting for 

> How can a SIMT processor pipeline be modified to extract parallelism between warps?

Adding on a warp scheduler, making cores have multiple register files?

> The warp scheduler chooses instructions to execute. What are its criteria for choosing and what other schemes could be implemented?

The only thing that decides this are whether the operands are ready. One could imagine a more complex scheduling system, with more things taken into account like branches, "priority" and dependencies, which might allow you to have warps that depend on each other — but these all add overhead and go against the core principle of GPU programming which is to parallelize simple computations over lots of data. 

### GPU memory

> What are the types of memory available within a GPU and what are their relative advantages or disadvantages?

 - local memory
	 - can be cached, external DRAM
 - shared memory
	 - high bandwidth, within each processor
 - global memory
	 - can be cached
 - constant memory
	 - in DRAM, but cached in special "constant" caches

### GPU programming

> What types of application best suit GPUs and how can you program to take advantage of the various forms of parallelism available?

As said before, you want many small independent units of execution, for example, a matrix multiplication, or a dot product. Things that use these a lot might be scientific computing and machine learning, or graphical rendering tasks. Depending on different tradeoffs, GPUs might be optimized for throughput or for latency — a GPU designed for playing games at a high frame rate would have different optimizations than a GPU designed for doing large-scale batch computations. 


### CUDA and OpenCL
> In CUDA, what’s the difference between a thread block and a warp?

A thread block contains warps. A thread block is a group of threads that are all executing the same instruction/set of instructions (kernel), and the thread block is divided up into warps for execution.

> Why does OpenCL require an application to discover the available platforms and devices?

Because OpenCL is portable across many possible architectures/GPUs, so the application needs to find the devices available to it.

> What’s the difference between an OpenCL `clFlush(queue)` and `clFinish(queue)`?

`clFlush` is asynchronous, meaning the CPU can continue doing things while the GPU receives and executes the commands in the queue. `clFinish` is blocking, so it waits for execution to finish.
> How do out-of-order queues in OpenCL avoid breaking dependences between commands when they rearrange them?

Each command has a wait list that says what events the command depends on. 

> Compare and contrast the OpenCL programming model with CUDA.

- OpenCL
	- more verbose
		- has to do more at runtime (e.g. device discovery)
		- compilation to GPU code is done at runtime as well
	- but more portable
		- can target many devices, even non-GPU devices like FPGAs
- CUDA
	- only targets NVIDIA GPUs
	- but can thus be compiled statically
	- and is less verbose

## further directions

> Why is energy efficiency the “new fundamental limiter of processor performance”, as Borkar and Chien say?

We're hitting the limit, not just with mobile chips but also with high-end chips, where it's becoming physically impossible to get enough cooling to squeeze performance out of energy-inefficient chips. 

### big.LITTLE

Arm's big.LITTLE system has some high-performance cores and some energy-efficient cores. This lets you be more energy efficient for less intensive workloads, and it also fits with the "sprint computing" idea where you drive a high-performance core very hot to finish a computation quickly, and it fits your thermal budget because the rest of the cores are inactive. Dynamically switching between these lets you get the benefit of high performance for tasks that need it, while not taking as much power overall. 

> When might it make sense to implement functionality in a specialised accelerator rather than within a general-purpose core?

For very common tasks that are sufficiently general in and of themselves — for example, video decoding — it makes sense to have a specialized accelerator. These can often be much more energy efficient than a general-purpose core, and can thus reduce the power requirements. Also, it depends on your system constraints. In a mobile setting, it might make sense to have lots of bespoke accelerators since phones have very purpose-built functionalities, and energy efficiency is very important. In a server setting, it might make less sense, since the space of possible tasks for the server might be much wider, and so it might be better to offer flexibility and more general-purpose performance rather than specialization.

> What types of application domain might benefit from approximate computing?

Graphics, where small errors might not be noticed. For machine learning inference, where perhaps sampling from a probability distribution can be done at lower precision, and the particular outputs are not as important. 