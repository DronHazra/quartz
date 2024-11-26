---
title: Nicola Cancedda at Cambridge
tags:
  - AI
  - talk
---
why interpret model internals?
- because we're curious,
- and for "prosaic" reasons ([[prosaic interpretability]])
	- mitigating hallucinations, jailbreaks etc
	- enhancing reliability
	- possible architectural improvements?
- and the explanations given by models for their own "thinking" are (consider reasoning traces being unfaithful)

the typical picture of transformers de-emphasizes the residual connections — but they're actually very important! residual stream is the *bus* (communication channel) for the model.

- the weight matrices either *read* or *write* to the residual stream
- [[linear representation hypothesis]] (hmm)
- and then RepE: controlling models by altering the parameters
	- ex stop a certain *write* matrix from editing a particular subspace (feature)


now talking about [[papers/Yu_et_al__2024__Robust_LLM_safeguarding_via_refusal_feature_adversarial_training|Robust LLM safeguarding via refusal feature adversarial training]]:

and [[papers/Cancedda - 2024 - Spectral Filters Dark Signals and Attention Sinks|Cancedda - 2024 - Spectral Filters Dark Signals and Attention Sinks]]
