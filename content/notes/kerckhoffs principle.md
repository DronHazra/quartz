---
title: kerckhoffs principle
tags:
  - definition
  - cryptography
---
for a system to be secure, it must not require secrecy — it can be stolen by the enemy without causing trouble. 

## notes
the original context for this principle was for military encryption (1883). today it is emphasized as **not relying on security by obscurity.** one way of modeling this is by considering the substantial effort involved in designing a new cryptographic algorithm. if the algorithm relies on its own secrecy to be secure, then if (or when) any instance is broken, you need to design a whole new algorithm. if instead there algorithm is published, standardized and battle-tested, a particular instance being broken simply requires a change of keys.

so this leads to things that we generally want out of cryptographic systems: 

- easy rekeying
- redistribution of keys
- fast revocation of compromised keys

