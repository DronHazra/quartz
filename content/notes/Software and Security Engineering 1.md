---
title: "Software and Security Engineering 1"
tags:
 - uni
 - exercises
 - sse
---
## multi-level security
> You are provided with a computer system which supports multi-level security with four levels (open, confidential, secret and top secret) and permits information to flow upwards only. In addition, it permits compartmentalization of any layer into one of five compartments (A, B, C, D and E) between which lateral flows are prohibited. Subjects are authenticated and the system supports rolebased access control, allowing a subject to act in one or more roles. Describe how you could use this system to support:
> 
> (a) an electricity utility with four power stations and
> 
> (b) medical records in a hospital with four departments. 
> 
> Comment on the suitability of your solutions in the provision of integrity, confidentiality, the different risks to different stakeholders and safety overall. In the case of medical records, what changes are required to accommodate researchers who want access to anonymised records, or clerks who want access to financial data on bed occupancy and the financial cost of care for each patient?

for the electricity utility:
 - the principals are:
	 - customers
	 - employees of each power station
	 - employees of the central utility
 - other stakeholders include:
	 - government
we implement the policy that:
 - a customer's power usage can be
	 - seen by:
		 - the customer
		 - employees authorised by customer
		 - "the government"
	 - edited by:
		 - no one
 - company data from a power center can be seen and edited by anyone working for that power center with appropriate clearance, or top-level executives
we define compartments for each power center, and one for customer data (say E for customer data). critical/proprietary information is top secret.

i'm not sure how to define all the interactions in the power company case — what data should i be protecting?

for the medical case:
 - patients and their doctors can see the patient's medical records
 - only doctors can modify medical records
 - nurses can see current treatment instructions and can *append* to medical records

we have one compartment for patient records, and another for all other records. patient records are designated top secret, and subjects must authenticate before accessing them. we use different roles for principals executing a treatment or prescribing a treatment. those executing a treatment (e.g. nurses) can read but not write. 

again, i can understand how the system might work, but i'm really unsure of what pieces of data to be protecting

## security policy for timetable
> Write a security policy for https://timetable.cam.ac.uk

an *event* is a lecture or practical, led by a *lecturer* as part of a *department*.

a student's timetable is a set of events taken from various courses. 

a lecturer's timetable is the set of events that they lead. 

a student $S$'s timetable can be:
 - edited by S
 - read by:
	 - $S$
	 - anyone who $S$ chooses to share read rights with

a lecturer $L$'s timetable can be:
 - edited by:
	 - $L$
	 - for events under deparment $D$, administrators of department $D$
 - read by:
	 - $L$
	 - all students
	 - all university and department administrators
## hacking a friend's account
 - convince them to go get a coffee, hoping they leave their laptop and phone unlocked
 - allow them to log in to their email on your laptop, and don't let them log out
	 - this of course assumes that they for some reason need to access their email on your laptop
 - offer help in setting up a development environment, and secretly install software that takes the gmail session token
 - suggest them a great productivity extension that writes emails for you, that also downloads all of their emails and sends them to you
 - threaten them
 - ask them to help you test a chrome extension you're working on. have it log them out of their gmail account and notify you. log the password and 2fa code they type in, and log in yourself.
## prospect theory
> Spend 10 minutes researching prospect theory and then write a short description.

prospect theory is the asymmetry of risk assessment when dealing with losses vs gains. it finds that people are generally risk-averse when considering gains, and risk-seeking when faced with losses. for example: if someone is faced with a 50% chance to win $1000 and 100% chance to win $400, they are more likely to choose the $400 despite it yielding less expected value. however, if they are faced instead with a 50% chance to lose $1000 and a 100% chance to lose $400, they are more likely to choose the former. 

## social psychology-based attacks
> Describe how a social psychology technique could be used to improve the likelihood of each of following types of attack. You should be able to use several different social psychology techniques for each scenario.
>  1. Tricking a user into visiting a specific website on their laptop 
>  2. Persuading a user to pay after their computer has been infected with ransomware
>  3. Disregarding advice on health and safety
>  4. Encouraging a user to install a dodgy app on their Android smartphone

1. Appeal to authority: fake an email from the Canadian Revenue Agency instructing users to click on the link to fix their tax filing. (The CRA is a trusted authority, people are more likely to listen to them.)
   
   Appeal to FOMO: send an email from an "investing" firm promising high returns if they sign up now by clicking the link, emphasizing how many people have already signed up and how time is running out. (People don't want to miss out on opportunities.)
   
   Appeal to dishonesty: on an adult website, have a popup that says "click the button below to verify your age", where the button directs to the link. (People are less suspicious of others if they themselves are doing something suspicious.)
2. Appeal to time pressure: threaten the user with a timer counting down to their data being stolen/PC being fully shut down, if they don't pay. (People take less time to think when under time pressure.)
   
   Appeal to dishonesty: threaten to leak personal info (e.g. browser history) if the user doesn't pay. (People may want to hide that they were vulnerable to ransomware, and so are more likely to pay. Particularly effective in enterprise settings, where a person's livelihood may be on the line.)
3. Appeal to FOMO: show pictures/videos of people doing the behaviour and having fun. (People don't want to miss out.)
   
   Appeal to authority: find or forge footage of doctors advising the mark to do the behaviour. (People are more likely to accept health advice that looks like a doctor)
   
   Appeal to kindness: say that it would really help this struggling elderly couple. (People can be convinced to break rules if they believe the are being altruistic)
4. Appeal to greed: pretend the app will give them free bitcoin. (People can be blinded by personal gain.)
   
   Appeal to distraction: hid the link to installing the app behind the "close" button of an mobile game advertisement. (People may mistakenly click on the link when trying to close the app.)
   
   Appeal to social proof: hack or otherwise coerce a friend of the mark to convince the mark to install the app. (People trust their friends.)

## raven password policy
A password must be at least 8 characters long, with all of: upper/lower-case letters, numbers, and symbols.

