---
title: concepts in programming languages 1
tags:
- uni
- exercises
---


## abstract machines
> What do we mean by abstract machine when describing a programming language? Outline the basic characteristics of the abstract machines of:
> - FORTRAN (the original 1957 variant)
> - LISP (the original McCarthy dialect) 
> - ALGOL68

For FORTRAN, we have a flat register machine, with memory modelled as a simple linear array. The machine is flat in the sense that we have no bounds on what memory we can access. It is also flat in the sense that we have no concept of a "call stack" or recursion, only top-level procedures. We also have no complex data structures in the language, only simple scalars that have fixed sizes (or strings/arrays, which must have a *fixed declared length*). It's designed this way to be as close as possible to the underlying hardware of the time, making compilation much easier. 

LISP's abstract machine is an "expression evaluator", something akin to the lambda calculus, where an S-expression is treated as a list `(function arg1 arg2 ...)`. Evaluating an expression means evaluating the arguments, and then substituting them into the function expression.

ALGOL68 expands Fortran's model to include a *stack* and a *heap*. The stack is used for local variables and function calls, and the heap is used for explicitly allocated variables. In particular, the stack and heap are both *dynamic*, unlike Fortran's entirely statically allocated storage. The abstract machine also includes lots of high-level constructs that we consider standard now, like:
- the machine being able to execute closures and handle higher-order functions
- the machine deciding what scope to access a variable from (lexical scoping)
- specification of parameter passing semantics (call by name or value)
- the machine doing garbage collection on heap storage

## compiling FORTRAN

> One of the most important factors in the design of FORTRAN was the ease of compiling it. Identify some aspects of the original FORTRAN abstract machine that make it a language that can be compiled down to efficient machine code. [Hint: think of the optimisations you mentioned in the Compiler Construction course.]

Compiling Fortran is easy in part because the machine model specified is so close to what might be targeted by machine code. All storage is statically allocated, so the compiler doesn't have to worry about where something is in memory — it can decide at compile time. There is no concept of scoping, and so a variable's name can easily be transformed into a set of registers or a set location in memory. We pass everything by reference, which means that operations within a function can simply done directly with the registers involved, rather than having to copy them. 

*Note:* also the execution state is the same when you call a function (e.g. using `GOTO`), so you don't need to e.g. save the state of the registers


## eval in LISP
*note:* performance considerations 

## encapsulation in Smalltalk

> A commonly used practice in object-oriented programming is encapsulation. You have already informally defined it in Object-Oriented Programming as ‘a class should expose a clean interface that allows full interaction with it, but should expose nothing about its internal state or how it manipulates it’. SIM- ULA 67 had no facilities to achieve encapsulation. How did Smalltalk improve on this? Comment on why encapsulation might be desirable.

Smalltalk offers *full encapsulation of all objects.* The only way to interact with an object in Smalltalk is to send a message to it. E.g. you never directly modify a data structure, you only send it messages. You don't add numbers, you send an `add` message to an `Integer` with another `Integer`.

Encapsulation is useful because it allows you to ensure that your code is only used in the way that it's expected to be used in. It means that underlying implementation details can be changed without changing the interface. For Smalltalk in particular, it seems very amenable to concurrent execution, since all behaviour takes place as message passing with no shared memory or state. 

*Abstraction* hides implementation details.

*Access modifiers* facilitates encapsulation.

## typing

> Please answer the following questions
> - (a) What do we mean by strong typing?
> - (b) Show how hard-to-find errors can result from the absence of strong typing.
> - (c) Distinguish static typing and dynamic typing.
> - (d) Is Java completely statically typed or completely dynamically typed?

Strong typing guarantees that a well-typed program will not error. 

An example is when you return a pointer to a stack-allocated struct in `C`. The type system will accept it, even though at runtime this will cause an error, since the stack-allocated struct will be deallocated when the scope ends.

Static typing means the types are decided at compile-time, while dynamic typing means the types are decided at runtime.

Java does a mix of both static and dynamic typing. All objects are assigned a type at compile-time, but they may have a different type at runtime due to subtyping. Dynamic dispatch also means we need some degree of dynamic typing, since the method called is determined by the object's runtime type.

## what is a scripting language?

a scripting language is one that has a REPL. 

## javascript

- A browser has a built-in JavaScript interpreter that interprets JavaScript on a webpage (or from the console).
- Callbacks are functions that are called when a certain event happens. For example, the `onClick` property on a button takes a callback that should be run whenever the button is clicked. 

