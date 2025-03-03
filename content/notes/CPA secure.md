---
title: CPA secure
tags:
  - definition
  - cryptography
aliases:
  - chosen plaintext attack
---
the chosen plaintext attack on a high level allows the attacker oracle access to the encryption procedure.

to formalize it as a security game:

the challenger generates a random bit $b$ and a key $K$. the adversary A gets oracle access to $\mathsf{Enc}_K$, so they send $M^1, M^2, \dots, M^t$ and get ciphertexts $C^1, C^2, \dots, C^t.$ The adversary then outputs (chooses) any two messages $M_0, M_1$. The challenger picks which one to encrypt based on $b$: $C \leftarrow \mathsf{Enc}_K (M_b)$ and returns $C$ to A. 