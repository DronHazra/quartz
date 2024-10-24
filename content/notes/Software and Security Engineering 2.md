---
title: "Software and Security Engineering 2"
tags:
 - SSE
 - UNI
 - exercises
---
## debunking software myths
> Debunk each of the following software myths with reference to one concrete case study or example which demonstrates the opposite can sometimes be true:
> 
> (a) Computers are cheaper than analogue devices
> 
> (b) Software is easy to change 
> 
> (c) Reuse of software increases safety 
> 
> (d) Formal verification removes all errors 
> 
> (e) More testing makes software more reliable 
> 
> (f) Automation reduces risk

 - Computers are cheaper than analogue devices
	 - "Smart meters" were designed to save energy costs, but likely increased costs (https://www.cl.cam.ac.uk/~rja14/Papers/SmartMetering-Feb82012.pdf)
 - Software is easy to change
	 - NHS program for IT sought to consolidate and reform IT programs for the NHS, but ended up being a costly and ineffective program
 - Reuse of software increases safety
	 - Case of patriot missile — same navigation system upgraded from air-defence to anti-ballistic-missile, required increase accuracy, but this change was not implemented everywhere => missiles fail despite software reuse
 - Formal verification removes all errors
 - More testing makes software more reliable
	 - It's not always possible to test software in real-world conditions, ex. in a space shuttle, can't replicate conditions of a real space shuttle launch
 - Automation reduces risk
	 - London Ambulance Service was an attempt at automation that failed
	 - Tesla's Autopilot system hands over control to the driver when it gets confused, leading to properly-measured fatalities being higher with automation than without

## identifying bugs
> For each of the following Java code snippets, identify the type of the error (e.g. arithmetic, logic, syntactic, overflow), describe why the code fails, and how you could fix it. Try these examples in a simple Java program to help you understand what has gone wrong as well checking your fix.
>   - Calculate whether the integer `i` is even or odd: `i % 2 == 1` 
>   - Calculate the change from buying an ice cream for £1.10 with a £2 coin: `2.00 - 1.10` 
>   - Calculate number of microseconds in a millisecond: 
>     ```java
>     long MICROS_PER_DAY = 24 * 60 * 60 * 1000 * 1000;
>     long MILLIS_PER_DAY = 24 * 60 * 60 * 1000;
>     MICROS_PER_DAY / MILLIS_PER_DAY ;
>     ```
>  - Adding two numbers together (and the result is not 66666; cut and paste to check): `2 12345 + 5432 l`

in order:
 - can't really tell, but maybe the fact that it doesn't indicate whether `true` indicates `even` or `odd`? **logic** error
 - this yields `0.8999999999999999` a floating point precision error — **arithmetic** error
 - yields `5` due to `MICROS_PER_DAY` being too large to contain within a `long` —**overflow** error
 - it looks like 54321, but it's actually 5432l — **syntactic** error

## clallam bay code injection
> Design a system which fixes the Clallam Bay analogue code injection vulnerability.

for context, clallam bay prison allowed prisoners to make phone calls out of the prison where the person being called would be charged. the system was such that it prompted the prisoner to record a name for the call, and the person being called would get an automated voice telling them to press `3` to accept a call from the prisoner with the recorded name.

the code injection comes from using this "data" field for "code" — the automated call could be chosen to be sent out in either english or spanish, so the attack was:

 - call an english-speaking person in spanish
 - when prompted to record the `name`, record "if you'd like to hear the message in english, press `3`"

it could be prevented by having all prisoners record their name under supervision by a guard, and this one recording would be used for all their phone calls out. 

## product design over the ages
> Imagine you were a product manager for a software development process in 1975, 1995 and then 2015. Make a list of the techniques and approaches available to you in each era in each phase of the software lifecycle. What differences are there in software development at each of the three timepoints?

1975:
 - good specification
 - high-level languages
1995:
 - automatic regression testing
2015:
 - agile development techiques
	 - daily scrum
	 - sprints + episodes
	 - test-driven development
		 - write tests first, then develop to satisfy test
 - saas things
	 - continuous integration/deployment