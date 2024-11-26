---
title: albert jiang
draft: "true"
---
reasoning and MoE

[[Mixture of Experts]]

## synthetic data and reasoning

math is often anti-AR, i.e. it's written in a style that doesn't lend itself to forward thinking — synthetic data is the bridge 

so! often times you get things like `question, answer, reasoning`, so you rewrite things to get `question, reasoning, answer`(just ask a reasonable language model to do this)

(this is from [orca math](https://arxiv.org/abs/2402.14830))

or you can tweak the question: `Q(a, b, ?), S(a, b, ?), A(c) -> Q(?, b, c), S(?, b, c), A(a)`, but sometimes this makes the problem much harder

or [STaR](https://arxiv.org/abs/2203.14465) (generate new solutions to old problems, and then verify that the answer is correct)