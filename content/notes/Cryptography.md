---
title: Cryptography
tags:
  - uni
  - notes
---
start with some specifications of what we want:
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

## encryption schemes
declaratively, we specify 3 things:

1. a key generator `Gen`
2. an encryption procedure `Enc`
3. a decryption procedure `Dec`

and we have goals to prevent adversaries from:
- finding the secret/private key
- find the plaintext `M`
- determine any bit of `M`
- determine any information about `M` from `C`
- compute any function of `M` from `C` ([[semantic security]])

and threat modelling:
- attacker has ciphertext
- and $(M, C)$ pairs
- and [[oracle access]] to enc or dec
- of varying degrees (how many applications of enc or dec?)
- has varying amounts of compute
- and varying knowledge of the algorithms used (see [[kerckhoffs principle]])

this is all to say that there are many definitions for what it means for a cryptographic system to be *secure*. 

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

here we can start with a simple taxonomy: [[computational security]] and [[unconditional security]]