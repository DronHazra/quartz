---
title: Cryptography
tags:
  - uni
  - notes
---
one of the themes of cryptography is formally defining what we mean by "secure". there are many things we might want to do. for example, in a [[symmetric encryption]], we might want to prevent adversaries from: 

- finding the secret/private key
- find the plaintext $M$
- determine any bit of $M$
- determine any information about $M$ from $C$ ([[notes/unconditional security|unconditional security]])
- compute any function of $M$ from $C$ ([[semantic security]])

and our adversaries might have different capabilities:
- attacker has ciphertext
- and $(M, C)$ pairs
- and [[oracle access]] to `Enc` or `Dec`
- of varying degrees (how many applications of `Enc` or `Dec`?)
- has varying amounts of compute
- and varying knowledge of the algorithms used (see [[kerckhoffs principle]])

we also have the different security properties we might want:
- confidentiality
	- information accessible only to those authorized
- integrity
	- ensuring information is accurate and complete, and that this is preserved when data is processed
- availability
	- authorized users have access to data/resources when required

each of these have attacks associated with them:
- confidentiality: eavesdropping (passive)
- integrity: middle-person (or man-in-the-middle, active)
- availability: DDoS

this is all to say that there are many definitions for what it means for a cryptographic system to be *secure*. 

in my view, this course separates into two main themes: **specifying what it means to be secure** and **constructing and composing primitives that satisfy these.** we will work primarily with [[security games]]. 

this course, as designed, focuses on some core techniques:
- [[notes/symmetric encryption|symmetric encryption]]
- [[message integrity]]
- [[hash functions]]
- [[asymmetric encryption]]
these connect to our goals above in different ways. 
## message integrity schemes
to verify that the message arrived intact, we need:
1. a key generator
2. message authentication code generator `Mac`

to verify that the message was sent by a particular person:
1. a key generator
2. signature generator `Sign`
3. signature verifier `Verify`

and again, we have goals to prevent adversaries:
- finding out the key
- create new $M'$ and a matching signature
- create new $M'$ that verifies as a given tag/signature (using a new signature)
- modify/recombine messages/tags such that they verify
- create two messages with the same signature

## key exchange schemes
classic diiffie hellman, but remember from SSE that this is vulnerable to spoofing... you don't know whether you're exchanging the key with the right person. 

different types of keys:
- private keys (shared but with specific people)
- public/secret key pairs (only you know the secret key)
	- note this isn't consistent: i had heard public/private key before
- ephemeral/session keys, generated fresh
	- this gives you [[forward secrecy]]
	- and also privacy, since you can't identify someone based off of constantly changing session keys
- static keys
	- stay unchanged for a while, usually for identity purposes
- master keys
	- used to generate other derived keys

# security definitions
one of the themes of this course so far is the emphasis on answering the question: *what is it that we mean by "secure"*?

here we can start with a simple taxonomy: 
![[computational security]] 

and ![[unconditional security]]

# rough notes (to be organized later)

[[negligible function]]

## modes of operation
- [[electronic codebook]]
- [[cipher block chaining]]
- [[cipher feedback mode]]
- [[output feedback mode]]
- [[counter mode]]