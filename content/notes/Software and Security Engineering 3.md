---
title: "Software and Security Engineering 3"
---
## not just integration tests
> Why don’t software engineers only use integration tests? Provide examples of circumstances in which other testing strategies are important.

you need unit tests to do test-driven development (where you write the tests and then code until the tests pass). integration tests don't test the behaviour of functionality in isolation which restricts the degree to which a single unit can be tested. having unit tests encourages healthy abstraction principles and maintaining loose coupling. also, integration tests are harder to write and reason about — this is wasted effort when what you want to test is local. also, if a test fails, it's difficult to tell where the failure occurred.

for example, consider a piece of code that does some physical calculation to set the throttle for a plane. only doing integration testing means that the physics calculation is never tested on its own, and so isn't verified to be correct in all the required cases.

## testing an e-commerce library
> A programmer creates an e-commerce library, however the project has some bugs and other shortcomings. You can download a copy [here](https://www.cl.cam.ac.uk/teaching/1718/SWSecEng/ecommerce.zip).

 - i imported the project into intellij and ran the unit tests that way.
 - notes on the library:
	 - `PaymentDetails` is used to allow for future flexibility if something else needs to be added to the payment details
	 - i'm not sure why `Order` exists. it potentially allows for more flexibility in the future, but it's still highly coupled to the `ShoppingCart` class (it uses `ShoppingCart`'s `paymentProcessor`).
	 - the `ShoppingCart` contains almost everything — it's a "god class". for example, there's no way to use the `Item` class outside of `ShoppingCart`, so displaying items in a GUI might be difficult
	 - we might want `CardPaymentProcessor.charge` to throw an exception if the payment fails, rather than relying on return codes
 - looking at the class for testing, we want to follow the "arrange act assert" paradigm. the `setup` method does this for us. the reason this is not done in a constructor is because the tests are being run by a testing library that would like to ensure the same preconditions for each test. we can get this by rerunning the setup method, rather than having to create a new instance of the class.
 - the second test doesn't assert anything about what the output should be — the order could return an empty string and it would still pass. similarly, it doesn't test whether the payment actually goes through. also, it tests multiple units of functionality — the `order.getNames()` method and the `order.chargePaymentCard()` method, which are logically different. 
 - the first test doesn't test adding an item to cart, so i added that.
 - dependency injection is a class getting objects which it needs as inputs rather than creating them itself
	 - it abstracts away creation/initialization of objects, so that the user of the object doesn't have to be changed when the implementation changes
	 - we can rewrite the `ShoppingCart` class, making the `Item` and `Order` classes separate, and having the `Order.chargePaymentCard` method take a `CardPaymentProcessor` as input.
