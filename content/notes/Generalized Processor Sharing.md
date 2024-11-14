---
title: Generalized Processor Sharing
tags:
  - definition
aliases:
  - GPS
---
some properties:
- work-conserving
- provides [[notes/max-min fairness|max-min fairness]] (or weighted!)
- visits flows round-robin
- it's a *fluid flow approximation*: serves an infinitesimally small amount of data from flow `i`.

as this is an approximate model (idealized), this provides upper bounds for fairness. you compare the fairness by