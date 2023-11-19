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

## extending MRSW

i've left in a bunch of process work under here, but here's the part that worked:

```C++
for(int x=p; x>=0; x--) {
	wait(free[x]);
}
//do work
for(int x=0; x <=p; x--) {
	signal(free[x]);
}
```

here higher-priority threads have lower `p`s. a lower priority thread must wait for all other thread of lower threads to clear out before they run.

of course, you have classic scheduling problems, like starvation — low priority threads may never run in this model. such as it is. 

---



i'd use another shared variable that tracks the highest priority thread waiting for a lock. ignoring all the read/write logic for now, it'd look something like this:

```C++
int nr = 0;
int max_prio = 0;
rSem = new Semaphore(1);
wSem = new Semaphore(2);
turn = new Semaphore(1);
plock = new Semaphore(1);
```

and then you'd have something like, assuming the thread priority is `p`,

```C++
wait(plock)
if(p > max_prio) {
	max_prio = p;
	signal(plock)
	wait(turn)
	// do work
	signal(turn)
}
else {
	//what.... to do here....
}
```

ok so that doesn't work, because what do you do if you aren't of high enough priority?

so instead we can have an array of binary semaphores all initialized to 1 for each priority level, indicating whether that priority slot is free or not. we'll still keep `max_prio` around so we know where to start counting down. 

```C++
wait(free[p]);
wait(plock);
max_prio = max(p, max_prio);
for(int i=max_prio; i>=0; i--) {
	signal(max_prio);
	wait(free[p])
}
while(p < max_prio) {
	signal(plock);
	wait(free[max_prio]);
	signal(free[max_prio]);
	wait(plock);
}
max_prio = max(p, max_prio);
signal(plock);
wait(free[p]);
wait(turn);
//do work
signal(turn);
signal(free[p]);


if (p > max_prio) {
	max_prio = p;
	signal(plock);
	wait(free[p]);
	// your priority gives you permission to enter the queue to 
	// do work
	wait(turn);
	// do work
	signal(turn);
	signal(free[p]);
}
else {
	int x = max_prio;
	while(x > p) {
		signal(plock);
		wait(free[x]);
		signal(free[x]);
		wait(plock);
		x = 
	}
	for(int x = max_prio; x >=p; x--) {
		// i guess... maxprio only goes up?
		wait(free[x]);
		signal(free[x]);
		x = max
	}
	// will only get here once all higher priority 
	wait(free[p]);
	
}
```

i'm trying this one more time, fresh. here's the plan:
 - there's a lock for each priority
 - whenever a thread wants to enter the protected section, they have to hold all the locks for all lower priorities. 
 - but, we want to make sure that, when a thread is of high priority and is waiting for a lock, threads of lower priority wait behind them
 - to facilitate this, we have threads acquire locks starting from the highest waiting priority. they must acquire and then release these locks.
 - once they have acquired and released all higher priority locks (confirming that no higher priority thread is waiting), they start acquiring and holding the rest of the locks
 - once they hold all the relevant locks, they do the work, and then release them.

when i tried to implement this, i also realized that we probably want this whole lock acquiring process to be critical, as in, only one thread should be iterating through locks at a time.

```C++
int max_prio = 0;
plock = new Semaphore(1);
free[] = [new Semaphore(1), ...]
```

```C++
wait(plock); //plock does double duty of protecting max_prio and our entire lock iteration process
max_prio = max(p, max_prio);
while(p < max_prio) {
	if(!try_wait(free[max_prio])) {
		signal(plock);
		wait(free[max_prio])
	}
	wait(free[max_prio]);
	wait(plock);
	max_prio--;
	signal(plock);
	signal(free[max_prio]);
}
while
```


ok one last try this is so annoying

```C++
for(int x=p; x>=0; x--) {
	wait(free[x]);
}
//do work
for(int x=p; x>=0; x--) {
	signal(free[x])
}
```

the issue with this is in the following:
 - $T_1$ (with priority 1, this stays the convention) comes in and starts doing work
 - then another thread $T_1'$ comes and waits
 - a thread $T_2$ with priority 2 comes in and waits
 - $T_1$ releases `free[1]` but this gives it to $T_1'$, and so on, and then $T_1'$ starts doing work
 - another thread of priority 1 could easily come again and again, and $T_2$ will simply have to wait for all the $T_1$'s

wait a second. what if we invert this priority system so that 0 is the highest priority. and we make it so that threads release the highest priority lock first

```C++
for(int x=p; x>=0; x--) {
	wait(free[x]);
}
//do work
for(int x=0; x <=p; x--) {
	signal(free[x]);
}
```


## await is problematic
`await()` can execute arbitrary computations, and this is bad. in particular, *when* do we run the computations specified in await? it might be nontrivial to tell when the condition being awaited is true — so we'd have compute the condition every time we wanted to check. if you do this each time the scheduler runs like e.g. `signal` in a semaphore, then the scheduler is now executing some arbitrary bit of user code — this is obviously bad because the process can then "steal cycles". we might instead make the thread spin, waiting for its condition, but this is inefficient. 

instead, we might force explicit condition variables that dont store any state. 