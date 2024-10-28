---
title: types
tags:
  - notes
  - uni
---

skipping a bunch of stuff to lecture 8 because that's when i started taking notes

- talked about adding references to the simply-typed lambda calculus
- but this breaks termination! because you can now build unbounded recursion => infinite loops
- the problem here is the interaction between *mutable state* and functions
- there are fancy ways to deal with this in e.g. core-safe rust and applying various restrictions on state
- but simpler is to use a [[monadic type system]]