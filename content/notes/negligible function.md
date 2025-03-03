---
title: negligible function
tags:
  - definition
  - cryptography
---
a function $f: \mathbb{N} \rightarrow \mathbb{R}_{\ge 0}$ is neglibile if for every polynomial $p$ there is an integer $N$ such that for all $n > N$, $f(n) < \frac{1}{p(n)}.$ 

this means that its output converges to zero faster than the inverse of any polynomial. 

it is normally written as `negl`. 