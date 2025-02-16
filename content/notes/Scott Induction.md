---
title: Scott Induction
tags:
  - definition
---
Scott induction packages together some reasoning that we can do with fixed points. Recall:

![[notes/Kleene fixed-point theorem|Kleene fixed-point theorem]]

So take $D$ and $f$ as above. Take $S\subseteq D$, or equivalently some predicate $\Phi$ on $D$. If S respects:

- $\bot$ (base case)
- $f$ (inductive step)
- chains (closure)

then $\text{fix}(f) \in S$. written out more explicitly:

- $\bot \in S$
- $f(S) \subseteq S$ 
- $\bigsqcup s_n \in S$

