---
title: diversified pipeline
tags:
  - definition
  - arch
---
instructions are issued in order but may complete out of order. we have a parallel sub-pipeline

## notes
- have to worry about write-after-write hazards
- have to worry about contention for register file write ports
- and as such we get more [[notes/structural hazard|structural hazards]]

## examples
ARM10 pipeline has multiple execution paths:
- ALU path (single-cycle)
- MUL path
- MEM path (for accessing memory)

notably this allows *independent* ALU instructions to bypass load/stores and execute anyway. hazards are checked late