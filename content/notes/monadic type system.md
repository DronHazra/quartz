---
title: monadic type system
tags:
  - notes
  - uni
---
a monadic type system adds a type $T\, X$ that says "this term is impure"

at least, that's a simple way of doing this

we're also going to add $\{t\}$ as a *suspended effectful computation*, i.e. you can make an impure computation pure by just not running it

and we're going to extend our typing judgements to be mutually recursive: split into pure typing judgements and effectful type judgements:

pure terms:

![[Pasted image 20241028112226.png]]

effect terms:

![[Pasted image 20241028112243.png]]

so we're introduction and elimination rules for the $\text{ref} X$ *monad*

and notably the fact that $\text{return }e$ doesn't have an effect means that we can promote pure computations to impure computations. monadic type systems are a *conservative approximation*, they assume that everything with the monad type is impure, and so anything that relies on that computation is impure, even if it's not. this means you can't encapsulate exceptions.

so now all our proofs are mutual inductions: we prove exchange and weakening mutually between pure and impure.

but, in fact, you can prove the pure versions of progress and preservations without mutually recursing, since $\{t\}$ is a value, so impure computations are never evaluated when evaluating pure terms.


