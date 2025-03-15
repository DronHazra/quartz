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

1. the challenger generates a random bit $b$ and a key $K$.
2. the adversary A gets oracle access to $\mathsf{Enc}_K$, so they send $M^1, M^2, \dots, M^t$ and get ciphertexts $C^1, C^2, \dots, C^t.$
3. the adversary then outputs (chooses) any two messages $M_0, M_1$.
4. the challenger picks which one to encrypt based on $b$: $C \leftarrow \mathsf{Enc}_K (M_b)$ and returns $C$ to A.
5. the adversary can continue to request encryptions, and then must output a prediction $b'$. the adversary succeeds if $b=b'$.

we denote this game as $\mathsf{PrivK}^{\mathsf{cpa}}_{\mathcal{A}, \mathsf{\Pi}} (\ell).$

> we say that a given private-key encryption scheme $\mathsf{\Pi}$ is CPA-secure if for all probabilistic, polynomial-time adversaries $\mathcal{A}$, there exists a [[notes/negligible function|negligible function]] $\mathsf{negl}$ such that $$\mathbb{P} (\mathsf{PrivK}^{\mathsf{cpa}}_{\mathcal{A}, \mathsf{\Pi}} (\ell) = 1) \le \frac 1 2 + \mathsf{negl} (l).$$

in diagram form: ![[Pasted image 20250303214711.png]]