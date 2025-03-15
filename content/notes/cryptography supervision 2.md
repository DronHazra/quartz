---
title: cryptography supervision 2
tags:
  - exercises
  - cryptography
  - uni
---
> In the CBC mode of operation, the initial vector (IV) is chosen uniformly at random, using a secure source of random bits. Show that CBC would not be CPA secure if the initial vector could be anticipated by the adversary, for example because it is generated instead using a counter or a time-stamp.

If the adversary could anticipate the initial vector, then CBC would be deterministic from the perspective of the adversary. Concretely, in the security game, if I could predict the initial vector for each message $C_0^t$, I could request encryption of the modified message with the first block $M_0' := M_0^t \oplus C_0^t$. When the challenger encrypts this, the initial vector cancels out — the rest of the process is fully deterministic, so this attack removes all nondeterminism from CBC. 

> Explain for each of the discussed modes of operation (ECB, CBC, CFB, OFB, CTR) of a block cipher how decryption works.

![[notes/electronic codebook|electronic codebook]]

![[notes/cipher block chaining|cipher block chaining]]

![[cipher feedback mode]]

![[output feedback mode]]


> A sequence of plaintext blocks $M_1, \dots, M_8$ is encrypted using DES into a sequence of ciphertext blocks. Where an IV is used, it is numbered $C_0$. A transmission error occurs and one bit in ciphertext block $C_3$ changes its value. As a consequence, the receiver obtains after decryption a corrupted plaintext block sequence $M_1', \dots, M_8'$. For the discussed modes of operation (ECB, CBC, CFB, OFB, CTR), how many bits do you expect to be wrong in each block $M_i$ ? (Hint: You may find it helpful to draw decryption block diagrams.)

![[Pasted image 20250305004519.png]]

![[Pasted image 20250305004534.png]]

![[Pasted image 20250305004555.png]]

> Your opponent has invented a new stream-cipher mode of operation for 128-bit key AES. He thinks that OFB could be improved by feeding back into the key port rather than the data port of the AES chip. He therefore sets $R_0 = K$ and generates the key stream by $R_{i+1} = E_{R_i} (R_0)$. Is this better or worse than OFB?

The problem here is that you generate your key only once, and this variant of OFB is deterministic given a certain key. This means that in the setup of the CPA game we had previously, this mode of operation is deterministic, so it can't be CPA secure — it's worse than OFB. 

In practice, relying on the key for both the encryption procedure and the nondeterminism for encrypting the blocks means that you can never encrypt multiple messages with the same key. This means you have to do a lot of key distribution, which is hard.