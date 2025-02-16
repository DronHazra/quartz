---
title: "Lipman et al. - 2022 - Flow Matching for Generative Modeling"
tags:
  - paper
---

## Links
- [PDF](http://arxiv.org/pdf/2210.02747v2)
- [arXiv](https://arxiv.org/pdf/2210.02747)

## Abstract

We introduce a new paradigm for generative modeling built on Continuous
Normalizing Flows (CNFs), allowing us to train CNFs at unprecedented scale.
Specifically, we present the notion of Flow Matching (FM), a simulation-free
approach for training CNFs based on regressing vector fields of fixed
conditional probability paths. Flow Matching is compatible with a general
family of Gaussian probability paths for transforming between noise and data
samples -- which subsumes existing diffusion paths as specific instances.
Interestingly, we find that employing FM with diffusion paths results in a more
robust and stable alternative for training diffusion models. Furthermore, Flow
Matching opens the door to training CNFs with other, non-diffusion probability
paths. An instance of particular interest is using Optimal Transport (OT)
displacement interpolation to define the conditional probability paths. These
paths are more efficient than diffusion paths, provide faster training and
sampling, and result in better generalization. Training CNFs using Flow
Matching on ImageNet leads to consistently better performance than alternative
diffusion-based methods in terms of both likelihood and sample quality, and
allows fast and reliable sample generation using off-the-shelf numerical ODE
solvers.

## notes

key objects:

given a vector field $v: \phi: [0, 1] \times \mathbb{R}^d \rightarrow \mathbb{R}^d$ (i.e. `v: time -> vec -> vec`), we have a *flow*: $\phi: [0, 1] \times \mathbb{R}^d \rightarrow \mathbb{R}^d$ that satisfies $$\frac{d}{dt} \phi_t (x) = v_t (\phi_t (x))$$and $$\phi_0(x) = x.$$this is obviously time-dependent, and it's a [[Diffeomorphism]]. for us, that's important because it means we can invert this process.

