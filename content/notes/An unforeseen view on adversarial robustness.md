---
title: An unforeseen view on adversarial robustness
---

I find myself explaining this a lot, so I wanted to write out a quick explanation of this line of though in adversarial robustness research. This is mostly a give-you-the-answers type post that's summarizing a few different papers. 

## security mindset and the $\varepsilon$-ball
the "starting point" i'm going to be using here is https://arxiv.org/abs/1706.06083 ([[notes/Towards Deep Learning Models Resistant to Adversarial Attacks|Towards Deep Learning Models Resistant to Adversarial Attacks]])

Say you have an image classification model $f_{\theta}$, an ImageNet model, you give it images and it gives you classifications. You know that networks can have weird failure cases, so you want to construct an *adversarial example*, an image chosen specifically to mess with your model.

The important idea is: we're looking for some kind of *worst case*. Within some reasonable set of inputs, we're looking for the model to be maximally wrong. We formulate this as an optimization problem: taking pairs $(x, y) \sim \mathcal{D}$

$$\mathbb{E}_{(x, y) \sim \mathcal{D}} \left[\max_{\tilde{x}\in \mathcal{S}_x} L(\theta, \tilde x, y)\right]$$

$$\mathcal{S}_x = \{\tilde x : ||\tilde x - x||_p \le \eps\}$$

We're going to use One Weird Trick, and we'll generalize it later. Take an image $x$ with target class $y$, compute the gradient of the loss function wrt your *input.* Perturb your input a tiny bit in that direction and voila, your network (maybe) gave the wrong answer. We're computing $\tilde{x} = x + \varepsilon \delta$ where $\delta = \text{sign}(\nabla_x \mathcal{L}(\theta, x, y))$. 


$$\tilde x = A(x, \delta)$$
$$S^{A, \eps}_x = \{A(x, \delta) |\,\; \vert\vert\delta\vert\vert_p \le \eps\}$$
$$\mathsf{UA2} = \frac{1}{|\SA|}\sum_{A\in \mathcal{A}} \text{Acc}(A, \eps_A, f)$$

$$\delta$$