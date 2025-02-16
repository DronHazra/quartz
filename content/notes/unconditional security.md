---
title: unconditional security
tags:
  - definition
  - cryptography
---
an information theoretic definition of security. 

> An encryption scheme over message space $\mathcal{M}$ is perfectly secret if for every probability distribution over $\mathcal{M}$, message $M$ and ciphertext $C$ with $P(C) > 0$, we have $$P(M|C) = P(M).$$

this express that knowing the ciphertext leads to *no new information* relative to the priors over $M$. even with unlimited computational power, no new information exists to be had. 