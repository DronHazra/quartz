---
title: cat theory
tags:
  - notes
  - uni
aliases:
  - category theory
  - CAT
---
define [[cartesian closed pre-order]]

so we'll link this with [[intuitionistic propositional logic]], and show that there's an isomorphism between IPL and a cartesian closed preorder

in particular, we'll draw the link between the *syntax* (of IPL) and the *semantics* (in a cartesian closed preorder). we'll do this by way of a *meaning function* $M$ that goes from syntax (formulas in IPL) to $P(, \sqsubseteq)$ (cc [[denotational semantics]]).

recurse on the structure of a formula to define $M \llbracket p \rrbracket$ 

we have pierce's law which is not provable in IPL. how do you show this? you can get a counter model in your *semantics*, i.e. find a cartesian closed poset where it does not hold. 

here we have a slightly new interpretation of *soundness* and *completeness*. 

> [!info]
> Soundness: syntax to semantics

> [!info]
> Completeness: semantics to syntax

as in [[notes/types|types]] we can draw the correspondence from IPL to the [[simply typed lambda calculus]], which means that we can again define a semantics in the same way: via a meaning function $M$. when we do this, we're doing this categorically, which lets us turn *variables* into *projections*. 

> [!note]
> Take the axiom $\Gamma, x:A \vdash$ 

in essence we can take all the *categorical universal properties* (of products and exponentials and terminal/initial elements), and since SLTC is syntax-directed (i.e. the structure of the term is the structure of the proof) this means that the categorical semantics *is the only way that you could define it*

common theme in category theory! specify something such that there really is only one possible way for something to happen (i.e. satisfies the universal properties). 

so this transforms the STLC into a language of *combinators*. 