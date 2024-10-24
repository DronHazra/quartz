---
title: "l-p metrics"
tags:
 - math
 - definition
---

https://en.wikipedia.org/wiki/Norm_(mathematics)#p-norm

norms of a vector space

the $p$-norm of a vector $\mathbf{x}$ is something like: $$||x||_p := \left(\sum_{i=1}^n |x_i|^p\right)^{1/p}$$

links to the notion of a [[metric space]], where we're defining a distance function for different vector spaces

ex: 
![[Pasted image 20230315141702.png]]

![[Pasted image 20230315141720.png]]

the euclidean metric is the $l_2$ norm, $||x||_2 = \sqrt{x_1^2 + x_2^2 + \dots + x_n^2}$

in particular, the $l_\infty$ metric is particularly useful. when the limit is taken, the biggest component of the vector dominates, so it goes to $(x_i^p)^{\frac 1 p} = x_i$, i.e. $\max x$
