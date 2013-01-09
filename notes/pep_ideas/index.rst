Various Ideas for Python and CPython
====================================

My ability to generate ideas for ways in which Python could potentially be
improved in various areas vastly outstrips the time I'm willing to spend
following up on them, kicking them around with other community members and
turning them into suggestions that may actually prove to be a genuine
enhancement to the language rather than just useless cruft new Python
programmers have to learn in order to understand code other programmers might
write.

As a result, there are plenty of ideas I've had that may actually
have some merit, but that I don't have the time to explore. Some of these
are going to be *bad* ideas that justifiably won't survive the
gauntlet of python-ideas and python-dev review, while others may make sense
as esoteric PyPI modules rather than as standard library or core language
additions.

Beyond that, there are many fascinating things *other* people are working
on, where I may be able to contribute some thoughts, but don't have the time
to get more directly involved. Those noted below are all core development
related - there are many fascinating things going on in the community and
education space, as well as at higher levels of the application stack
(especially in web development and scientific computing) but in those
spaces I truly am just an observer (albeit one that is enthusiastically
cheering on those doing the work).

.. note: Some of these articles are just placeholders for the moment. In
   those cases, they have a link to relevant python-ideas posts or past blog
   posts.


Current Activities
------------------

These are things I am currently working on directly.

Working on the CPython startup sequence is currently fairly painful, and
it can also be hard to tweak appropriately when embedding CPython in a
larger application. I'm currently working on a plan to do something
about that for Python 3.4:

* :pep:`432` (simplifying the CPython startup sequence)

Potentially following on from that are various ideas people have had (most
notably Graham Dumpleton) to make subinterpreters more robust. I'm
considering following up PEP 432 with additional work on that, including
`making better use of the cyclic GC`_ when destroying modules (which should
help with misbehaviour at interpreter shutdown, but needs to be done with
great care to avoid creating ridiculous amounts of uncollectable garbage).

The test helpers in our regression test suite currently suffer from
discoverability problems, so I've been working with Chris Jerdonek to
make test.support a package, and move the helpers out from their current
location as peer modules of the regression tests themselves. Chris has
a series of patches on the tracker for this, and we're just waiting for
the final 3.2 maintenance release to be published before we apply them.

Finally, I've been taking an active interest in Daniel Holth's work on the
binary ``wheel`` format and related PEPs (I am now the BDFL delegate with
final approval rights over these PEPs):

* :pep:`425` (binary compatibility tags)
* :pep:`426` (updated package metadata format)
* :pep:`427` (the ``wheel`` format itself)

.. _making better use of the cyclic GC: http://bugs.python.org/issue812369

Help Needed
-----------

These are things I'd quite like to see happen for 3.4, but I'm not
actively working on them and, as far as I'm aware, neither is anyone else:

* `Bytes and Text Transform API`_ (``codecs.encode`` and ``codecs.decode``)
* `Changing IO encodings`_ (mostly for stdin/stdout/stderr)
* :pep:`422` (a simple class initialisation hook)
* importlib based support for post-import hooks (see :pep:`369`)
* `Python level buffer API`_ (based on the enhanced :class:`memoryview` in 3.3+)
* `Multi-dimensional memoryview indexing and slicing`_
* `Fixing operand precedence`_ for sequences implemented in C
* `Improved disassembly tools`_

.. _Bytes and Text Transform API: http://bugs.python.org/issue7475#msg165435
.. _Changing IO encodings: http://bugs.python.org/issue15216
.. _Python level buffer API: http://bugs.python.org/issue13797
.. _Multi-dimensional memoryview indexing and slicing: http://bugs.python.org/issue14130
.. _Fixing operand precedence: http://bugs.python.org/issue11477
.. _Improved disassembly tools: http://bugs.python.org/issue11816

I think the first two items above will close a couple of important gaps in
the Python 3 unicode support, while the third will resolve a regression in
language capability that complicates the porting of some code from Python 2.
PEP 422 would also make certain forms of metaprogramming significantly
simpler to read, write and use. (I'm actually talking to someone about
handing over the reins for PEP 422)

Lazy loading of modules is something pretty much every large Python
command line application reinvents in order to improve startup times. With
``importlib`` now used as the basis for the import system, it would be good
to take advantage of that to add a robust post-import hook mechanism.

The others are miscellaneous gaps in language functionality and problems
with CPython's implementation that aren't causing major dramas at the moment
but would still be nice to clean up.

However, they don't impact me directly the way the startup and test
suite issues do, so they drop a bit further down my personal priority list.


Other Interests
---------------

Other people are working on things where I'm an interested observer,
contributing my thoughts but not specifically driving the process in
any way:

* Vinay Sajip and others are working on ``distlib``, a new approach to
  providing better stdlib infrastructure for packaging and distribution for
  3.4 (after the failed attempt based on ``distutils2`` for 3.3)
* Antoine Pitrou is working on :pep:`428`, a possible higher level API for
  access to various aspects of file and filesystem manipulation
* Antoine is also working on :pep:`3154`, a new version of the pickle
  protocol (which should have some flow-on benefits for multi-processing)
* Lennart Regebro is working on :pep:`431`, bringing political timezone
  support directly into the standard library
* Guido van Rossum is working on :pep:`3156`, a standardised API for
  explicitly asychronous code

There are also rather a lot of `tracker issues I am following`_, although
my level of interest in those varies greatly :)

.. _tracker issues I am following: http://bugs.python.org/issue?@columns=title,id,activity,nosy,status&@sort=-activity&@group=priority&@filter=nosy,status&@pagesize=50&@startwith=0&status=1&nosy=1309&@dispname=My%20Nosy%20List

In relation to Guido's async PEP, I had a few suggestions that he felt
weren't appropriate for the PEP itself. For lack of a better location,
I've posted them here:

.. toctree::
   :maxdepth: 2

   async_programming.rst


Tinkering with Ideas
--------------------

These are other ideas that I'm actually working on (albeit intermittently).

I have two deferred drafts in the main PEP index, which are competing
ideas to allow Python to represent thoughts that follow the mathematical
pattern of "let <name> = <expression> where <define subexpressions>" in
that order in addition to the current algorithmic order, just as we allow
both recursive and iterative implementations of algorithms, and the use of
both classes and closures for scoping, etc:

* :pep:`403` (the ``@in`` decorator clause)
* :pep:`3150` (the ``given`` statement local namespace clause)

(These are deferred because I think there are larger problems in the grand
scheme of things, but "we want something like Ruby blocks" is also a topic
that comes up fairly regularly, so it's useful to have these available as
a focus for any discussions. I currently have a slight preference for the
``@in`` clause as I think it suitably targets the niche I am interested in,
and better integrates with existing language concepts like decorators)

The following ideas are ones which I don't even consider baked enough to
put together as PEPs. I may also decide not to submit them (primarily if
someone else decides to run with them first or if I decide they're a bad
idea after all)

.. toctree::
   :maxdepth: 2

   release_cadence.rst
   core_packaging_api.rst


Ideas for PyPI Prototype Packages
---------------------------------

This section is for ideas that could conceivably be implemented as a package
on the Python Package Index, and hence should be field tested in that
environment before incorporation into the standard library can be seriously
considered.

.. toctree::
   :maxdepth: 2

   codec_pipeline.rst
   strview.rst

My own ``walkdir`` and ``shell-command`` packages fit here. They're
mostly languishing because I'm not sure the ideas underlying them are
actually all that solid.

Dubious Ideas
-------------

This section is for ideas that would require changes to the Python language
definition. All such proposals are deemed dubious by default - ideas that
would make the core Python language definition better are vastly
outnumbered by those that would make it worse :)

.. toctree::
   :maxdepth: 2

   suite_expr.rst
   implicit_with.rst
   ast_metaprogramming.rst


Past Ideas
----------

These are archived ideas that were either elaborated into full PEPs, or
which I now actively consider to be a bad idea:

.. toctree::
   :maxdepth: 2

   skip_with.rst
   preview_namespace.rst

