---
title: advanced computer architecture
tags:
  - uni
  - notes
---
chiplets:
 - yield for big dies is low, yield for small dies is high (because chance of defect is the same but you have to throw away a small die vs big die?)

## pipelining
so in a non-pipelined processor, we have CPI of 1 (good!) but also our clock period will be slow (since it has to respect the worst-case time + margin).

when we pipeline, we have some overhead for adding pipeline registers (ff). each extra FF is like an extra constant c, so our period goes from $T+C$ to $T/2 + 2C$, so there is actually a tradeoff. you have to account for clock skew and timing requirements for your pipeline registers — important for very deep pipelines

when you stick pipeline registers in your machine, you kind of want:
- pipeline registers that isn't too wide (not too much to carry over)
- divides delay evenly

notably register files have many ports to support high-bandwidth access (esp on superscalar processors)

in the ideal pipeline case, you have a CPI of 1 (no stalls). e.g.

`pipelined CPI = ideal pipeline CPI + pipeline stalls/instruction`

### pipelining hazards
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
- 
