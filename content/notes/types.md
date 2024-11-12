---
title: types
tags:
  - notes
  - uni
---

## datatypes
$\mathbb{N}$ is specified by zero and successor, there are two ways to introduce (construct) it, (zero and successor), and to eliminate you do primitive recursion

(the eliminator has the already consumed subterm)

## system F
so we generalize our types from pure trees to "binding" trees (because we now have type variables). $$A::= A\rightarrow B | \alpha | \forall \alpha. A$$
and so we need a typing context $\Theta \vdash A \, \mathrm{type}$. the typing context $\Theta$ is just a list of type variables $\alpha, \beta$ and so on. 

$\Lambda$ is how you take type variables in program terms

so church encodings are... defined by the elimination form? we want to be able to eliminate, for ex, booleans into an arbitrary types using `if`. so: $$\mathrm{bool} := \forall \alpha. \alpha \rightarrow \alpha \rightarrow \alpha$$
this encodes the fact that we take two values of type $\alpha$ (one for each case) and return one of them. 

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

ok! so now we can try to prove progress and preservation for lamba-mu

we can prove preservation just fine, we don't even need induction (try it!)

but when we try to prove progress, we find that we can't actually write down any "closed contradictions" — i.e. we can't write any programs of continuation type without free variables.

possibly linked to the fact that you often need "truth tables" to interpret things in classical logic? like if you need truth tables, that means that you have free variables, for each free variable you test both true and false, and that's what gives you the semantics of the logic. but constructive logic is purely syntactic, we can define the semantics recursively on the syntax..?

neel claims you can make classical logic into a subset of constructive logic. unsure how. let's find out:

we start by talking about double-negation elimination. you don't have double negation elimination in constructive logic. but you *do actually* have triple negation elimination, i.e. *double negation is irrefutable.* we can write down a program: $$\lambda k. \lambda a. k (\lambda q. q\, a)$$
check that this has the correct type!

we also define quasi-negation ($\sim A = A \rightarrow p$) for some fixed arbitrary type $p$, to avoid the fact that there are either 0 or 1 functions from $A \rightarrow 0$. 

now what we want to do is *embed* classical logic into constructive logic using triple negation — i.e. define a translation function that takes a classical logic formula and turn it into a constructive one. the point is that the classical logic formulae will be equivalent, but the constructive logic ones won't necessarily be equivalent..?

a translation function takes a type $A$ and translates it to $A^\bullet$. 

## normalization

the syntactic technique does not work because the structure of a $\lambda$-term does not say anything about the expression contained within

so we introduce some extra machinery — the [[Fundamental Lemma of Type Theory]] 

the logical relations

reducibility candidate 