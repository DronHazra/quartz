---
title: branch prediction
tags:
  - uni
  - notes
  - arch
---
note that not all processors want branch prediction, especially if you want tight control over delay:
- real-time things like video decoders
- secure chips where you want all your operations to take the same amount of time
	- branch predictors are often [[side channels]]

ARM10 branch prediction unit:
- ARM10 allowed two instructions per cycle to be *fetched*
- so the branch predictor could predict before that instruction was even computed
- *branch folding*
- static branch predictor

- simple, one-level, one-bit predictor
	- hash branch address into table
	- predict that we do the same thing as we did last time
	- problem is that you usually get two mispredictions (e.g. on loop exit and entry)
- simple, one-level, two-bit predictor
	- very simple: add a lag before you flip prediction ([[hysteresis]])
	- 2-bit saturating counters
- more than two bits (with more complex state machines) is not very useful

we can also add in some *history*, or a two-level predictor:
- take advantage of local history, store it in a table, and then concat
	- so you query your table with (branch id, history)
- you can also use global history (global in the sense of *any* branch taken rather than particular branch taken)

some further techniques:
- tournament predictors
	- local and global predictors, and
	- a predictor that that chose whcih one
- dealing with aliasing


