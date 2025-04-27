---
title: security games
tags:
  - definition
  - cryptography
---
one of the ways we define security is via the rules of a game played between two players. a challenger, who presents some kind of scheme $\mathsf{\Pi}$, and an adversary $\mathcal{A}$ who tries to demonstrate some weakness in the scheme. we write this as $X_{\mathcal{A}, \mathsf{\Pi}}(\ell)$, where $\ell$ is a security parameter to scale the difficulty. this parameter is required for our complexity-theoretic notion of [[notes/computational security|computational security]].

usually, it goes like this:

1. the challenger uniformly picks at random a secret bit $b$
2. $\mathcal{A}$ interacts with the challenger according to the rules of the game
3. $\mathcal{A}$ outputs a bit $b'$ (a *guess*)

if $b=b'$, $\mathcal{A}$ wins and $X_{\mathcal{A}, \mathsf{\Pi}}(\ell) = 1$. the loss is analogous. 

a scheme $\mathsf{\Pi}$ is $X$ secure if, for all [[probablistic polynomial-time]] adversaries $\mathcal{A}$, there exists a [[notes/negligible function|negligible function]] $\mathsf{negl}$ such that $$X_{\mathcal{A}, \mathsf{\Pi}}(\ell) = 1 < \frac 1 2 + \mathsf{negl}(\ell).$$