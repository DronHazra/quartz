---
title: register renaming
tags:
  - definition
---
basically the thing we do here is renaming the set of registers for each stream of instruction execution, like, something where the compiler is always going to use the same registers for things like function return address, and its always going to put locals in the same spot — but we can map the "logical" (microarchitectural registers) to many physical registers and map between them accordingly. this is "renaming". something something rotating the rotating register file richard talked about it

