---
title: "Yu et al. - 2024 - Robust LLM safeguarding via refusal feature adversarial training"
tags:
  - paper
---

## Abstract

Large language models (LLMs) are vulnerable to adversarial attacks that can
elicit harmful responses. Defending against such attacks remains challenging
due to the opacity of jailbreaking mechanisms and the high computational cost
of training LLMs robustly. We demonstrate that adversarial attacks share a
universal mechanism for circumventing LLM safeguards that works by ablating a
dimension in the residual stream embedding space called the refusal feature. We
further show that the operation of refusal feature ablation (RFA) approximates
the worst-case perturbation of offsetting model safety. Based on these
findings, we propose Refusal Feature Adversarial Training (ReFAT), a novel
algorithm that efficiently performs LLM adversarial training by simulating the
effect of input-level attacks via RFA. Experiment results show that ReFAT
significantly improves the robustness of three popular LLMs against a wide
range of adversarial attacks, with considerably less computational overhead
compared to existing adversarial training methods.

## notes

- take harmful/harmless pairs, plotting the representations in 2-D pca separates them neatly
- jailbreaks shift the harmful examples towards the harmless ones (in 2-D pcas)
	- correlational / probing example
	- look at how the centroids move
- so you do a causal intervention
	- run an adv attack
	- and then restore the value of the "refusal direction"
- now you can use this to do adversarial training without adversaries!
	- ablate (subtract) the refusal direction instead of attacking the model
	- for harmful requests, train the model to refuse despite the refusal feature being ablated (randomly, with some probability)
- ReFAT model learns to keep "semantically similar" comment to the normal model's response, but still refuses task
- notably this doesn't need inference-time interventions
	- **self note:** most labs don't love retraining models! it's super expensive! inference-time interventions are comparatively cheap/less risky

## Links
- [PDF](http://arxiv.org/pdf/2409.20089v1)
- [arXiv](https://arxiv.org/abs/2409.20089)
