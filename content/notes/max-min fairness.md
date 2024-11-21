---
title: max-min fairness
tags:
  - definition
---
Every flow either receives what they demand, or share equally with all other flows that did not receive what they asked for.

Formally:
- $N$ is the total number of flows
- $x_n$ is the resource demand by flow $n$
- $C$ is the capacity
- $m_n$ is the actual resource allocation to flow $n$

So we have $$M_n = \frac{C - \sum\limits_{i=1}^{n-1} m_i}{N - n + 1}$$as the resource available to flow $n$. The way to read this is "an equal share of the capacity that's left." Then $m_n = \min (x_n, M_n)$. If you ask for less than what your fair share would be, you get your demands met. Otherwise, you get an equal share of what's available. 

Notably, **the flows must be sorted for this algorithm to work** (as stated anyway). 