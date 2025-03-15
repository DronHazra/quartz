---
title: cipher feedback mode
tags:
  - definition
  - cryptography
aliases:
  - CFB
---
cipher feedback mode (CFB) is another mode of operation for a block cipher. a weakness of [[notes/cipher block chaining|CBC]] is a full block is required before the ciphertext can be sent, which CFB attempts to improve. 

1. start with a random initial vector $C_0$ as in [[notes/cipher block chaining|CBC]]. 
2. output $C_i := M_i \oplus E_K (C_{i-1})$

note that once $C_{i-1}$ is computed, the block cipher step for $C_{i}$ can be computed immediately — no waiting for $M_{i}$ required. this means that as bits of $M_i$ arrive, we can encrypt them immediately without waiting for the block to fill.

an ancillary advantage is that we don't have to pad the last block.