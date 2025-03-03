---
title: advanced computer architecture
tags:
  - uni
  - notes
---
chiplets:
 - yield for big dies is low, yield for small dies is high (because chance of defect is the same but you have to throw away a small die vs big die?)

predictors are everywhere in high performance processors because they have *so many transistors*
# pipelining
so in a non-pipelined processor, we have CPI of 1 (good!) but also our clock period will be slow (since it has to respect the worst-case time + margin).

when we pipeline, we have some overhead for adding pipeline registers (ff). each extra FF is like an extra constant c, so our period goes from $T+C$ to $T/2 + 2C$, so there is actually a tradeoff. you have to account for clock skew and timing requirements for your pipeline registers — important for very deep pipelines

when you stick pipeline registers in your machine, you kind of want:
- pipeline registers that isn't too wide (not too much to carry over)
- divides delay evenly

notably register files have many ports to support high-bandwidth access (esp on superscalar processors)

in the ideal pipeline case, you have a CPI of 1 (no stalls). e.g.

`pipelined CPI = ideal pipeline CPI + pipeline stalls/instruction`

## pipelining hazards
in the non-superscalar case, we have pretty simple hazards:
- data hazard (data dependencies)
- control hazard (branch dependencies)
- structural hazard (resource requirement)
	- notably, one might ask "why ever have structural hazards?" the answer is that there are *tradeoffs*. we can add more ports to our register file but that costs things

in the superscalar case (trying to execute things out of order), we have *true* and *false* data dependencies. false data dependencies are *name* dependencies, where instructions reuse the same registers. we normally solve this [[register renaming]]

a more complete taxonomy is:
- read after write
- write after write
- write after read


inserting stalls/bubbles also has overhead! to reduce these, you designate pipeline stages that can't stall, and either:
- signal only the first stage to stall, and buffer incoming instructions (skid buffer)
- or replay instructions (see blackparrot)

it's difficult to guarantee that all instructions execute in the same clock cycle, so we can extend our execute stage with multiple different pipelines.

take the blackparrot:

TODO: look at blackparrot

![[diversified pipeline]]

### control hazards
- branches are hard since they're evaluated in the execute stage, so they require the following instructions to be turned into NOPs
- assuming branch is not taken
	- is easy because its simple
- evaluate the branch earlier
	- i.e. in the decode stage
	- necessitates very simple branch logic, and more forwarding paths (from previous mem/wb to *decode* now, since the branch might required)
	- reduces branch penalty to single cycle
- delayed branch
	- assert: instruction after branch is always executed, called the [[branch delay slot]]
	- largely ineffectual these days because of branch predictors
- [[branch prediction]]



## analyzing pipelines

- you have critical path of delay $T$. divide it into $S$ stages and add some clocking overhead, since each stage requires timing constraints on the registers, and possible clock skew — so you get $T/S + C$ as the new clock period
- assume further that stalls happen at frequency $b$, and assume the cost $\propto S$
- the clocking overhead and stalls mean that there is some optimal pipeline depth
- this is *shallower* if $b$ or $C$ is high
	- reducing $b$ (reducing structural hazards, better branch prediction etc) or $C$ (more aggressive clock tree, faster registers) but this costs *transistors*
	- more transistors => more area, more power
- optimize for area => shallower pipeline
- optimize for performance => deeper pipeline (see pentium 4 in 2004, 31 stages!)
- optimize for power => shallower pipeline

