The Lazy Dev's Guide to Testing Your Web API
============================================

Ryan Kelly


Love/Hate Testing?
------------------

Quality assurance = diminishing returns

Early testing efforts rewarded with great improvements

Tests get harder, improvements get more obscure

Process improvement!

Better testing tools to do more with less effort

Invest in laziness!

Be pro-actively lazy!
(And I clearly need to re-read Moving Pictures!)

What does Ryan know?
--------------------

- Mozilla web services (Firefox Sync Server)

- Tools (WebTest, WSGIProxy, FunkLoad)

- enthusiast, not yet expert

WSGI
----

- webtest = WSGI for humans

- drive a WSGI application in a temporary in-process environment

Demo
----

Using webtest to ensure the API operates as expected

Many helpers to perform useful function tests

WSGIProxy
---------

In-memory WSGI "app" that maps WSGI requests to HTTP requests

Can easily run webtest based functional tests against an out-of-process
web server

Repurpose functional tests as integration tests and deployment tests

Can pick up anything that goes wrong during deployment

Can use as a basis for simple load testing

FunkLoad
--------

Wants to be a monolithic "do everything" test framework

Standard mode of use requires that tests be implemented specifcally for
FunkLoad (this annoys Ryan, just demoing it to illustrate the point)

Can gather benchmarking data

Use benchmarking tools, as they deal with problems you may not have
thought of yet (e.g. only recording data while under full load, ignoring
ramp up and ramp down periods)

Nice report generation tools

FunkLoad + WebTest
------------------

Write an adapter between webtest API and FunkLoad API

Can then reuse *any* of your webtest based tests as a FunkLoad test

Can use to get differential results to see how your response times are going

Distributed Mode
----------------

Spin up clients on multiple hosts

Aggregate benchmarks from multiple clients

Other Approaches
----------------

Write FunkLoad tests, use WSGI-Intercept to redirect to in-process
WSGI application

Q & A
-----

Just some specific questions about FunkLoad and making in-process WSGI
calls on a live application

My Thoughts
-----------

Not a lot to add! Some of the ideas here seem similar to those in
django-sanetesting, but it in a way that doesn't drive the
inheritance model of the test suite. I may look at migrating
the PulpDist tests over to webtest (depending on how complex it is to
get the in-process Django environment up and running)