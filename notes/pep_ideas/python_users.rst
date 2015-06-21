Python's Users
==============

One of the reactions we sometimes get to various things we work on for Python
is one of incredulity: "Why on Earth are you wasting your time on X? Problem
Y is far more important!".

The answer is typically "because the relative importance of X and Y depends
on your point of view, and I currently consider X to be the more important
of the two" (although "because I find working on X to be more fun and interesting
than working on Y" is another common reason).

Assessing the relative importance of different changes to the language
involves making assumptions regarding the way the language is used. As
core developers, we actually have a pretty decent view into how it gets
used in practice, and many of us also have the experience and contacts to
know how it gets used by the silent majority of developers operating behind
corporate and government firewalls (of both the civilian and military
variety) rather than participating in the open source development community.

However, we don't make a habit of articulating the different users we're
trying to design for, so it's not surprising that the common answer of
"this is not for you" isn't recognised in advance.

The various sections of this essay try to go over the different groups I
keep in mind when working on CPython, my current perspective on how well I
think those groups are served by the Python community (as of 18 March 2013),
and where I see support for those groups currently heading.


Optimise for Maintenance
------------------------

One of Guido's key insights into language design is that code is read far
more often than it is written, so it makes more sense to optimise for
software maintenance than it does to optimise for starting from an empty
file. This means that readability is highly prized in the language design,
and brevity is favoured only insofar as it improves readability.


Individual Automation
---------------------

These users represent the classic "scripting" use case that gives scripting
languages their name. Traditionally associated with system administrators,
this role encompasses any individual that uses Python to automate aspects
of their own activities, without necessarily sharing those tools with
anyone else.

The line between individual automation and system integration is a
complex one. Often a script may start life as an individual automation
tool and then later become a critical workflow tool as it is shared amongst
a group.

There are many characteristics of CPython (such as the large standard library)
that are useful for this group


System Integrators
------------------

Scientists and Data Explorers
-----------------------------s

Internet Application Developers
-------------------------------

Corporate Internal Developers
-----------------------------

Educators and Students
----------------------
