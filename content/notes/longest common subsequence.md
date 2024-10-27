---
title: longest common subsequence
tags:
  - definition
---
given two sequences you want to find the longest common subsequence. formally, if you have sequences $v = v_1 v_2 \dots v_m$ and $w = w_1 w_2 \dots w_n$, you want to find indices $i_1 \dots i_t$ and $j_1 \dots j_t$ to satisfy:

- $v[i_a] = w[j_a]$ for all $a$, and 
- $t$ is maximized

note that subsequences of a string do not have to be contiguous: they are not substrings.

this is a canonical dynamic programming problem, where you can iteratively build a solution from solutions to sub-problems, and these sub-problems *overlap*. here, the table you build is the length of the longest common subsequence of a prefix of $v$ and $w$. so we populate our table:

$$
s[i, j] = \max(s[i-1, j], s[i, j-1], s[i-1, j-1])
$$
these correspond to the recursive cases:
- last character doesnt match: recursively find LCS with either last of $v$ or last of $w$ chopped off
- last character matches: include this in a candidate LCS, and recursively find LCS with last of $v$ and $w$ chopped off

this can be thought of as taking steps in the "edit graph" between two strings. 


