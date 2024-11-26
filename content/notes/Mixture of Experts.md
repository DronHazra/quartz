---
title: Mixture of Experts
tags:
  - definition
  - AI
---
- duplicating the MLPs and route representations via a "routing" layer
- you save compute relative to having a bigger MLP
- which gives you better inference properties (better long context, tend to do better multilingually)
- something maybe about initialization behaviour?
	- overtrained base models are good targets for duplication (upcycling https://arxiv.org/abs/2410.07524)
- 