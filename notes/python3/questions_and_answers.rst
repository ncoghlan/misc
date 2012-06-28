Python 3 Q & A
==============

Last Updated: 28th June, 2012

With the recent release of Python 3.3 beta 1, some questions are once again
being asked as to the sanity of the core Python developers. A few years ago,
we embarked down the path of asking the entire language ecosystem to
migrate to a new version that introduces backwards incompatible changes
that more obviously benefit future users of the language than they do
current users.

I've seen variants of these questions several times of the years, and
figured I'd 

The views expressed below are my own. While many of them are shared by
other core developers, and I use "we" in several places where I believe
that to be the case, I don't claim to be writing on the behalf of every
core developer on every point.

I am also not writing on behalf of the Python Software Foundation (of which
I am a nominated member) nor on behalf of Red Hat (my current employer).

TL;DR Version
-------------

* Yes, we know this migration is disruptive.
* Yes, we know that some sections of the community have never personally
  experienced the problems with the Python 2 Unicode model that this
  migration is designed to eliminate
* Yes, we know that many of those problems had already been solved by
  some sections of the community to their own satisfaction.
* Yes, we know that by attempting to fix these problems in the core Unicode
  model we have broken many of the workarounds that had been put in place
  to deal with the limitations of the old model
* Yes, we are trying to ensure there is a smooth migration path from Python
  2 to Python 3 to minimise the inevitable disruption
* No, we did not do this lightly
* No, we do not see any other way to ensure Python remains a viable
  development platform as developer communities grow in locations
  where English is not the primary spoken language.

It is my perspective that the web and GUI developers have the right idea:
dealing with Unicode text correctly is not optional in the modern world.
In large part, the Python 3 redesign involved taking Unicode handling
principles elaborated in other parts of the community and building them
into the core design of the language.


Why was Python 3 made incompatible with Python 2?
-------------------------------------------------

To the best of my knowledge, the initial decision to make Python 3
incompatible with the Python 2 series arose from Guido's desire to solve
one core problem: helping *all* Python applications to handle Unicode
text in a more consistent and reliable fashion without needing to rely
on third party libraries and frameworks. Even if that wasn't Guido's
original motivation, it's the rationale that *I* find most persuasive.

The core Unicode support in the Python 2 series has the honour of being
documented in PEP 100.
It was created as `Misc/unicode.txt`_ in March 2000 (before the
PEP process even existed) to integrate Unicode 3.0 support into Python 2.0.
Once the PEP process was defined, it was deemed more appropriate to capture
these details as an informational PEP.

Guido, along with the wider Python and software development communities,
learned a lot about the best techniques for handling Unicode in the six years
between the introduction of Unicode support in Python 2.0 and inauguration
of the `python-3000 mailing list`_ in March 2006.

One of the most important guidelines for sane Unicode handling is to ensure
that all encoding and decoding occurs at system boundaries, with all
internal text processing operating solely on Unicode data. The Python 2
Unicode model doesn't follow that guideline: it allows implicit decoding
at almost any point where an 8-bit string encounters a Unicode string, along
with implicit encoding at almost any location where an 8-bit string is
needed but a Unicode string is provided.

The reason this approach is problematic is that it means the traceback for
an unexpected :exc:`UnicodeDecodeError` or :exc:`UnicodeEncodeError` in a
large Python 2.x code base almost *never* points you to the code that is
broken. Instead, you have to trace the origins of the *data* in the failing
operation, and try to figure out where the unexpected 8-bit or Unicode code
string was introduced. By contrast, Python 3 is designed to fail fast in
most situations: when a :exc:`UnicodeError` of any kind occurs, it is more
likely that the problem actually does lie somewhere close to the operation
that failed. In those cases where Python 3 doesn't fail fast, it's because
it is designed to "round trip" - so long as the output encoding matches
the input encoding (even if it turns out the data isn't properly encoded
according to that encoding), Python 3 will aim to faithfully reproduce the
input byte sequence as the output byte sequence.

Ned Batchelder's wonderful `Pragmatic Unicode`_ talk/essay could just as
well be titled "This is why Python 3 exists".

Python 3 also embeds Unicode support more deeply into the language itself.
With UTF-8 as the default source encoding (instead of ASCII) and all text
being handling as Unicode, many parts of the language that were previously
restricted to ASCII text (such as identifiers) now permit arbitrary Unicode
characters. This permits developers with a native language other than
English to use names in their own language rather than being forced to use
names that fit within the ASCII character set.

Removing the implicit type conversions also made it more practical to
implement the new internal Unicode data model for Python 3.3, where
the internal representation of Unicode strings is automatically adjusted
based on the highest value code point that needs to be stored (see
`PEP 393`_ for details).

.. _Misc/unicode.txt: http://svn.python.org/view/python/trunk/Misc/unicode.txt?view=log&pathrev=25264
.. _python-3000 mailing list: http://mail.python.org/pipermail/python-3000/
.. _PEP 393: http://www.python.org/dev/peps/pep-0393/
.. _Pragmatic Unicode: http://nedbatchelder.com/text/unipain.html


OK, that explains Unicode, but what about all the other incompatible changes?
-----------------------------------------------------------------------------

The other backwards incompatible changes in Python 3 largely fell into the
following categories:

* dropping deprecated features that were frequent sources of bugs in
  Python 3, or had been replaced by superior alternatives and retained
  solely for backwards compatibility
* reducing the number of statements in the language
* replacing concrete list and dict objects with more memory efficient
  alternatives
* renaming modules to be more PEP 8 compliant and to automatically use C
  accelerator when available

The first of those were aimed at making the language easier to learn, and
easier to maintain. Keeping deprecated features around isn't free: in order
to maintain code that uses those features, everyone needs to remember them
and new developers need to be taught them. Python 2 had acquired a lot of
quirks over the years, and the 3.x series allowed such design mistakes to be
corrected.

While there were advantages to having ``print`` and ``exec`` as statements,
they introduced a sharp discontinuity when switching from the statement forms
to any other alternative approach (such as changing ``print`` to
``logging.debug`` or ``exec`` to ``execfile``), and also required the use of
awkward hacks to cope with the fact that they couldn't accept keyword
arguments. For Python 3, they were demoted to builtin functions in order
to remove that discontinuity and to exploit the benefits of keyword only
parameters.

The increased use of iterators and views was motivated by the fact that
many of Python's core APIs were designed *before* the introduction of
the iterator protocol.
That meant a lot unnecessary lists were being created when more memory
efficient alternatives were now possible.
We didn't get them all (you'll still find APIs that unnecessarily return
concrete lists and dictionaries in various parts of the standard library),
but the core APIs are all now significantly more memory efficient by default.

As with the removal of deprecated features, the various renaming operations
were designed to make the language smaller and easier to learn. Names that
don't follow standard conventions need to be remembered as special cases,
while those that follow a pattern can be derived just be remembering the
pattern. Using the API compatible C accelerators automatically also means
that end users no longer need to know about and explicitly request the
accelerated variant, and alternative implementations don't need to provide
the modules under two different names.

No backwards incompatible changes were made just for the sake of making them.
Each one was justified (at least at the time) on the basis of making the
language either easier to learn or easier to use.


When can we expect this disruption to largely be over?
------------------------------------------------------

Going in to this process, my personal estimate was that
it would take roughly 5 years to get from the first production ready release
of Python 3 to the point where its ecosystem would be sufficiently mature for
it to be recommended unreservedly for all new Python projects.

Since 3.0 turned out to be a false start due to its IO stack being unusably
slow, I start that counter from the release of 3.1: June 27, 2009.
At time of first writing (June 28, 2012), that puts us 3 years into the
process, with the 3.3 release just a few months away. If we haven't put this
largely behind us by the end of June, 2014, I'll be disappointed. 

In the past year or so, key parts of the ecosystem have successfully made
the transition. NumPy/SciPy is now supported in both versions, as are
several GUI frameworks. The Pyramid web framework is supported, as is the
py2exe Windows binary creator.

There is a `Python 2 or Python 3`_ page on the Python wiki which aims to
provides a more up to date overview of the current state of the transition.

I think Python 3.3 is a superior language to 2.7 in almost every way. There
are still a couple of rough edges where certain text and binary data
manipulation operations are less convenient than they are in 2.7, but I
hope to see those squared away for 3.4 (which will still be within my 5
year window).

In terms of the overall ecosystem, some key milestones I personally hope
to see within this year or in 2013 are Python 3 compatible versions of
Twisted, Django and wxPython (all 3 have some level of migration effort
in progress).

Support in enterprise Linux distributions is also a key point for uptake
of Python 3. Canonical have already shipped a supported version (Python 3.2
in Ubuntu 12.04 LTS) with a stated goal of eliminating Python 2 from the
live install CD for 12.10. A Python 3 stack has existed in Fedora since
Fedora 13 and has been growing over time, but Red Hat has not made any
public statements regarding the possible inclusion of that stack in a future
version of RHEL.

To give some other perspectives on the transition, I'll note that Ubuntu
already has a `tentative plan`_ to move their Python 2 stack into the
community supported "universe" repositories and only officially support
Python 3 for their 14.04 release.

The Arch Linux team have gone even further, making Python 3 the
`default Python`_ on Arch installations. I am `dubious`_ as to the wisdom
of that strategy at this stage of the transition, but I certainly can't
complain about the vote of confidence!

.. _Python 2 or Python 3: http://wiki.python.org/moin/Python2orPython3
.. _tentative plan: https://wiki.ubuntu.com/Python
.. _default Python: https://www.archlinux.org/news/python-is-now-python-3/
.. _dubious: http://www.python.org/dev/peps/pep-0394/


Python 3 is meant to make Unicode easier, so why is <X> harder?
---------------------------------------------------------------

At this point, the Python community as a whole has had more than 12 years
to get used to the Python 2 way of handling Unicode. For Python 3,
we've only had a production ready release available for 3 years. Even in
the core development team, we're still coming to terms with the
full implications of a strictly enforced distinction between binary and
text data.

Since some of the heaviest users of Unicode are the web framework developers,
and they've only had a viable WSGI target since the release of 3.2, you can
drop that down to less than 2 years of intensive use by a wide range
of developers with extensive practical experiencing in handling Unicode (we
have some *excellent* Unicode developers in the core team, but feedback from
a variety of sources is invaluable for a change of this magnitude).

That feedback has already resulted in major improvements in the Unicode
support for both Python 3.2 and 3.3, and that process will continue
throughout the 3.x series.

In addition, we're forcing even developers in strict ASCII-only environments
to have to care about Unicode correctness, or else explicitly tell the
interpreter not to worry about it.

I've written more extensively on both of these topics in
:ref:`binary-protocols` and :ref:`py3k-text-files`.


Didn't you strand the major alternative implementations on Python 2?
--------------------------------------------------------------------

Cooperation between the major implementations (primarily CPython, PyPy,
Jython, IronPython, but also a few others) has never been greater than
it has been in recent years.
The core development community that handles both the language definition
and the CPython implementation includes representatives from all of those
groups.

The language moratorium that severely limited the kinds of changes
permitted in Python 3.2 was a direct result of that collaboration - it
gave the other implementations breathing room to catch up to Python 2.7.
That moratorium was only lifted for 3.3 with the agreement of the development
leads for those other implementations. Jython is lagging further behind
than others, with a 2.7 release due out soon, but the key feature of Jython
is using Python code to script the *Java* ecosystem, reducing the importance
of compatibility with the Python ecosystem for components with a Java
equivalent. Significantly, one of the most disruptive aspects of the 3.x
transition for CPython and PyPy (handling all
text as Unicode data) was already the case for Jython and IronPython, as
they use the string model of the underlying JVM and CLR platforms.

We have also instituted `new guidelines`_ for CPython development which
require that new standard library additions be granted special dispensation
if they are to be included as C extensions without an API compatible Python
implementation.

Python 3 specifically introduced :exc:`ResourceWarning`, which alerts
developers when they are relying on the garbage collector to clean up
external resources like sockets. This warning is off by default, but
switched on automatically by many test frameworks. The goal of this warning
is to detect any cases where ``__del__`` is being used to clean up a
resource, such as a file or socket or database connection. Such cases are
then updated to use either explicit resource management (via a
``with`` or ``try`` statement) or else switched over to :mod:`weakref` if
non-deterministic clean-up is considered appropriate (the latter is quite
rare in the standard library). The aim of this effort is specifically to
ensure that the entire standard library will run correctly on Python
implementations that don't use refcounting for object lifecycle management.

Finally, Python 3.3 has converted the bulk of the import system over to pure
Python code so that all implementations can finally start sharing a common
import implementation. Some work will be needed from each implementation to
work out how to boostrap that code into the running interpreter (this was
one of the trickiest aspects for CPython), but once that hurdle is passed
all future import changes should be supported with minimal additional effort.

.. _language moratorium: http://www.python.org/dev/peps/pep-3003/
.. _new guidelines: http://www.python.org/dev/peps/pep-0399/


Aren't you abandoning Python 2 users?
-------------------------------------

We're well aware of this concern, and have taken what steps we can to
mitigate it.

First and foremost is the extended maintenance period for the
Python 2.7 release. We knew it would take some time before the Python 3
ecosystem caught up to the Python 2 ecosystem in terms of real world
usability. Thus, the extended maintenance period on 2.7 to ensure it
continues to build and run on new platforms. While python-dev maintenance
of 2.7 is slated to revert to security-fix only mode in just over 2 years
time (July 2015), even after python-dev upstream maintenance ends, Python 2.6
and Python 2.7 will still be supported by enterprise Linux vendors until at
least 2020 (and likely later in the case of 2.7).

We have also implemented various mechanisms which are designed to ease the
transition from Python 2 to Python 3. The ``-3`` command line switch in
Python 2.6 and 2.7 makes it possible to check for cases where code is going
to change behaviour in Python 3 and update it accordingly.

The automated ``2to3`` code translator can handle many of the mechanical
changes in updating a code base, and the `python-modernize`_ variant
performs a similar translation that targets the (large) common subset of
Python 2.6+ and Python 3 with the aid of the `six`_ compatibility module.

`PEP 414`_ was implemented in Python 3.3 to restore support for explicit
Unicode literals primarily to reduce the number of purely mechanical code
changes being imposed on users that are doing the right thing in Python 2
and using Unicode for their text handling.

So far we've managed to walk the line by persuading our Python 2 users that
we aren't going to leave them in the lurch when it comes to appropriate
platform support for the Python 2.7 series, thus allowing to perform the
migration on their own schedule as their dependencies become available,
while doing what we can to ease the migration process so that following our
lead remains the path of least resistance for the future evolution of the
Python ecosystem.

`PEP 404`_ (yes, the choice of PEP number is deliberate - it was too good
an opportunity to pass up) was created to make it crystal clear that
python-dev has no intention of creating a 2.8 release that backports
2.x compatible features from the 3.x series. After you make it through
the opening Monty Python references, you'll find the explanation
that makes it unlikely than anyone else will take advantage of the "right
to fork" implied by Python's liberal licensing model: we had very good
reasons for going ahead with the creation of Python 3, and very good
reasons for discontinuing the Python 2 series. We didn't decide to disrupt
an entire community of developers just for the hell of it - we did it
because there was a core problem in the language design, and backwards
compatibility break was the only way we could find to solve it once and
for all.

.. _python-modernize: https://github.com/mitsuhiko/python-modernize
.. _six: http://pypi.python.org/pypi/six
.. _PEP 414: http://www.python.org/dev/peps/pep-0414/
.. _PEP 404: http://www.python.org/dev/peps/pep-0404/


Aren't you concerned Python 2 users will abandon Python over this?
------------------------------------------------------------------

Certainly - a change of this magnitude is sufficiently disruptive that
many members of the Python community are legitimately upset at the impact
it is having on them.

This is particularly the case for users that have never personally been
bitten by the broken Python 2 Unicode model, either because they work
in an environment where almost all data is encoded as ASCII text
(increasingly uncommon, but still not all that unusual in English speaking
countries) or else in an environment where the appropriate infrastructure
is in place to deal with the problem even in Python 2 (for example, web
frameworks hide most of the problems with the Python 2 approach from
their users).

However, we have done everything we can to make migrating to Python 3 the
easiest exit strategy for Python 2, and provided a fairly leisurely time
frame (at least by open source volunteer supported project standards)
for the user community to make the transition. Even after full
maintenance of Python 2.7 ends in 2015, source only security
releases will continue for some time, and, as noted above, I expect
enterprise Linux vendors to continue to provide paid support for
some time after community support ends.


Doesn't this make Python look like an immature and unstable platform?
---------------------------------------------------------------------

Again, many of us in core development are aware of this concern, and
have been taking active steps to ensure that even the most risk averse
enterprise users can feel comforting in adopting Python for their
development stack, despite the current transition.

Obviously, much of the content in the previous two questions regarding the
viability of Python 2 as a development platform, with a clear future
migration path to Python 3, is aimed at enterprise users. Government agencies
and large companies are the environments where risk management tends to come
to the fore, as the organisation has something to lose. The start up and
open source folks are far more likely to complain that the pace of Python
core development is *too slow*.

The main change to improve the perceived stability of Python 3 is that
we've started making greater use of the idea of "documented
deprecation". This is exactly what it says: a pointer in the documentation
to say that a particular interface has been replaced by an alternative we
consider superior that should be used in preference for new code. We
have no plans to remove any of these APIs from Python - they work, there's
nothing fundamentally wrong with them, there is just an updated alternative
that was deemed appropriate for inclusion in the standard library.

Programmatic deprecation is now reserved for cases where an API or feature
is considered so fundamentally flawed that using it is very likely to cause
bugs in user code. An example of this is the deeply flawed
``contextlib.nested`` API which encouraged a programming style that would
fail to correctly close resources on failure. For Python 3.3, it has finally
been replaced with a superior incremental ``contextlib.ExitStack`` API which
should support similar functionality without being anywhere near as error
prone.

Secondly, code level deprecation warnings are now silenced by default. The
expectation is that test frameworks and test suites will enable them (so
developers can fix them), while they won't be readily visible to end users
of applications that happen to be written in Python.

Finally, and somewhat paradoxically, the introduction of `provisional APIs`
in Python 3 is a feature largely for the benefit of enterprise users. This
is a documentation marker that allows us to flag particular APIs as
potentially unstable. It grants us a full release cycle (or more) to ensure
that an API design doesn't contain any nasty usability traps before
declaring it ready for use in environments that require rock solid
backwards compatibility guarantees.

.. _provisional APIs: http://www.python.org/dev/peps/pep-0411/


Why wasn't *I* consulted?
-------------------------

Technically, even the core developers weren't consulted: Python 3 happened
because the creator of the language, Guido van Rossum, wanted it
to happen, and Google paid for him to devote half of his working hours to
leading the development effort.

In practice, Guido consults extensively with the other core developers, and
if he can't persuade even us that something is a good idea, he's likely to
back down. In the case of Python 3, though, it is our collective opinion
that the problems with Unicode in Python 2 are substantial enough to
justify a backwards compatibility break in order to address them, and
that continuing to maintain both versions in parallel indefinitely would
not be a good use of limited development resources.

We as a group also continue to consult extensively with the authors of other
Python implementations, authors of key third party frameworks, libraries and
applications, our own colleagues and other associates, employees of key
vendors, Python trainers, attendees at Python conferences, and, well, just
about anyone that cares enough to sign up to the python-dev or python-ideas
mailing lists or add their Python-related blog to the Planet Python feed,
or simply rant about Python on the internet such that the feedback
eventually makes it way back to a place where we see it.

Some notable changes within the Python 3 series, specifically PEP 3333 (which
updated the Web Server Gateway Interface to cope with the Python 3 text
model) and PEP 414 (which restored support for explicit Unicode literals)
have been driven primarily by the expressed needs of the web development
community in order to make Python 3 better meet their needs.

If you want to keep track of Python's development and get some idea of
what's coming down the pipe in the future, it's all
`available on the internet`_.

.. _available on the internet: http://docs.python.org/devguide/communication.html


But, but, surely fixing the GIL is more important than fixing Unicode...
------------------------------------------------------------------------

While this complaint isn't really Python 3 specific, it comes up often
enough that I wanted to put in writing why most of the core development
team simply don't see the GIL as a particularly big problem.

First and foremost, we have a general view that threading with shared
non-transactional memory is a broken model for general purpose concurrency.
Armin Rigo has explained that far more eloquently than I can in the
introduction to his `Software Transactional Memory`_ work for PyPy.

The advantages of GIL-style coarse grained locking for the CPython interpreter
implementation are that it makes naively threaded code more likely
to run correctly, greatly simplifies the interpreter implementation (thus
increasing general reliability and ease of porting to other platforms) and
has almost zero overhead when running in single-threaded mode for simple scripts
(since the GIL is not initialised until the threading support is imported,
or initialised via the C API, the only overhead is a boolean check to see if
the GIL has been created).

The *only* downsides of this approach are that it means that CPU bound Python
code can't scale to multiple cores within a single machine using threads, and
that IO operations can incur unexpected additional latency in the presence of
a CPU bound thread.

For IO bound code (with no CPU bound threads present), or, equivalently, code
that invokes external libraries to perform calculations (as is the case for
most serious number crunching code, such as that using NumPy and/or Cython),
the GIL has no significant impact: a single core can handle all Python
execution on the machine, with other cores either left idle
(IO bound process) or busy handling calculations (external library
invocations).

For seriously concurrent problems, a free threaded interpreter also doesn't
help much, as it is desired to scale not only to multiple cores on a single
machine, but to multiple *machines*.
As soon as a second machine enters the picture, threading based concurrency
can't help you: you need to use a concurrency model (such as a shared
database or a message queue) that allows information to be passed between
processes, either on a single machine or on multiple machines.

That's why there's no strong motivation to implement fine-grained locking in
CPython:

* a coarse-grained lock makes threaded code behave in a less surprising
  fashion
* a coarse-grained lock makes the implementation substantially simpler
* a coarse-grained lock imposes negligible overhead on the scripting use case
* fine-grained locking provides no benefits to single-threaded code (such as
  end user scripts)
* fine-grained locking may break end user code that implicitly relies on
  CPython's use of coarse grained locking
* fine-grained locking provides no substantial benefits to event-based code
  that uses threads solely to provide asynchronous access to external
  synchronous interfaces (such as web applications using an event based
  framework like Twisted or gevent, or GUI applications using the GUI event
  loop)
* fine-grained locking provides no substantial benefits to code that
  uses other languages like Cython, C or Fortran for the serious number
  crunching (as is common in the NumPy/SciPy community)
* fine-grained locking provides no substantial benefits to code that needs
  to scale to multiple machines, and thus cannot rely on shared memory for
  data exchange
* a refcounting GC doesn't really play well with fine-grained locking (
  primarily from the point of view of high contention on the lock that
  protects the integrity of the refcounts, but also the bad effects on
  caching when switching to different threads and writing to the refcount
  fields of a new working set of objects)

The only case where free-threading *might* help is in applications where:

* CPU bound calculations are performed in Python code
* process-based concurrency techniques are not considered an acceptable
  substitute

Given the dubious payoff, and the wide array of effective alternatives, is
it really that surprising that the GIL isn't seen as the big problem it
is often made out to be? We're not an OS kernel - we have the option of
farming work out to a separate process if the GIL is a problem for a
particular workload. Sure, it's not ideal, and if a portable, reliable,
maintainable free-threaded implementation was dropped in our laps we'd
certainly seriously consider adopting it. Back in reality, though,
complaining about the GIL as though its a serious barrier to adoption
amongst developers that know what they're doing often says more about the
person doing the complaining than it does about CPython.

Some significant work did go into optimising the GIL behaviour for Python
3.2, and further tweaks are possible in the future as more applications are
ported to Python 3 and get to experience the results of that work, but
more extensive changes to the CPython threading model are highly likely to
fail the risk/reward trade-off.


.. _Software Transactional Memory: http://morepypy.blogspot.com.au/2011/08/we-need-software-transactional-memory.html
.. _further tweaks: http://bugs.python.org/issue7946
