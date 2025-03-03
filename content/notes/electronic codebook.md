---
title: electronic codebook
tags:
  - definition
  - cryptography
---
the simplest way to use a block cipher to encrypt an arbitrary-length message. it's very simple:
1. pad your message to a multiple of the block length
2. apply the block cipher to each block

this is is bad. notably, it is **not [[CPA secure]]** 