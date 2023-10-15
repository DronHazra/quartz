---
title: "Towards Deep Learning Models Resistant to Adversarial Attacks"
tags:
 - AI
 - paper
 - rough
---


https://arxiv.org/pdf/1706.06083.pdf

ok so the idea here is we want to apply security mindset to safety against adversarial attacks. 

providing guarantees for how safe a model is, against what attacks, against what strength of said attacks

specifying an attack model:

> $$\max_{\delta \in \mathcal{S}} L(\theta, x + \delta, y)$$

this is the general formalization of what it means, in this setup, to attack a model. the adversary wants to find the perturbation $\delta$ in some allowed set of perturbations $\mathcal{S}$ such that the loss $L$ of the model is maximized (here the model has parameters $\theta$). 

this doesn't really specify anything, but this gives us levers to change in defining our attacks. a popular choice for $\mathcal{S}$ is the $l_\infty$-ball around $x$.  (cc: [[l-p metrics]])


[[Fast Gradient Sign Method | FGSM]] is a way to actually get 
