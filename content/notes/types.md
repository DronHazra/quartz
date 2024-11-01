---
title: types
tags:
  - notes
  - uni
---

skipping a bunch of stuff to lecture 8 because that's when i started taking notes

- talked about adding references to the simply-typed lambda calculus
- but this breaks termination! because you can now build unbounded recursion => infinite loops
- the problem here is the interaction between *mutable state* and functions
- there are fancy ways to deal with this in e.g. core-safe rust and applying various restrictions on state
- but simpler is to use a [[monadic type system]]


so far in the course, we've been working in *constructive* logic ([[constructive logic]]) — i.e. we have negations only as $A \rightarrow 0$. notably this means that many laws in classical logic don't hold. an example is the law $\neg\neg A \iff A$ — this does not hold in constructive logic (try it! construct a lambda term in the simply-typed lambda calculus? you'll find that you'll need to write down a value of type $0$, which we don't have.)  

so what would it mean to include some more laws in our type system? what if we have true and false contexts? we're going to remove implication and add negation to our propositions (since implication can be implemented using negation, in classical logic). the rules here are somewhat similar to the [[sequent calculus]].

we then expand our notion of "proofs" with "refutations". proofs mean you judge a formula to be true, a refutation judges a formula to be false, and a contradiction means your true and false contexts contradict each other. 

notably the proof systems for refutations and proofs are quite symmetrical. proof strategies for $A$ correspond to refuting $\neg A$. *but this still doesn't get us to classical logic!* currently this proof system doesn't let you extract hypotheses from your assumptions. so we take a step forward, and let our rules make use of contradiction (an elimination rule). we're essentially allowing proof by contradiction here, which means we've left the realm of constructive logic for sure. to introduce a contradiction, we need to prove that a formula is both false and true. 

now let's turn this into actual terms in a programming language! 

er.... don't really understand this yet but i'll get there. but some interesting things to think about later:

- the evaluation rules look pretty similar to sequent calculus
- evaluation of this lambda-mu type theory is nondeterministic, it doesn't evaluate the same way every time (evaluation order matters)
- apparently, this is a calculus for *stack machines* i.e. CPS?? "static single assignment form"

