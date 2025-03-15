---
title: cipher block chaining
tags:
  - definition
  - cryptography
aliases:
  - CBC
---
cipher block chaining is a way to nondeterministically encrypt an arbitrary-length message using a block cipher.
1. pad your message to a multiple of the block length
2. generate a random *initial vector* (IV) $C_0$. this is the first ciphertext.
3. before encrypting block $M_i$, XOR it with $C_{i-1}$, i.e. $C_i := E_K (M_i \oplus C_{i-1})$
4. and then output the ciphertext $C := C_0 || C_1 || \dots || C_m$.

in diagram form:
![[Pasted image 20250303211456.png]]

note that you expect to see a block cipher input repeated after $\sqrt{2^n}$ blocks have been encrypted with the same key $K$, where $n$ is the block size in bits (TODO: why? so what?)