PEP Ideas: Free to a good home
==============================

My ability to generate ideas for ways in which Python could potentially be
improved in various areas vastly outstrips the time I'm willing to spend
following up on them, kicking them around with other community members and
turning them into suggestions that may actually prove to be a genuine
enhancement to the language rather than just useless cruft new Python
programmers have to learn in order to understand code other programmers might
write.

As a result, there are plenty of ideas I've had that may actually
have some merit, but that I don't have the time to explore. Be aware that
some of these are going to be *bad* ideas that justifiably won't survive the
gauntlet of python-ideas and python-dev review, while others may make sense
as esoteric PyPI modules rather than as standard library or core language
additions.

.. note: Several of these articles are just placeholders for the moment. In
   those cases, they have a link to relevant python-ideas posts or past blog
   posts. Explore a little - these are generally things I've written a fair
   bit about in the past.

PEP Drafts
----------

These are ideas that I'm actually working on (perhaps intermittently). They're
here to cut down on noise on the python-checkins list until they're in a
form suitable for submission to python-dev review. I may also decide not
to submit them (primarily if someone else decides to run with them first or
if I decide they're a bad idea after all)

.. toctree::
   :maxdepth: 2

   release_cadence.rst
   core_packaging_api.rst

In addition to the above drafts, I have two deferred drafts in the main
PEP index, which are competing ideas to allow Python to represent thoughts
that follow the mathematical pattern of "let <name> = <expression> where
<define subexpressions>" in that order in addition to the current
algorithmic order, just as we allow both recursive and iterative
implementations of algorithms, and the use of both classes and
closures for scoping, etc:

* :pep:`403` (the ``@in`` decorator clause)
* :pep:`3150` (the ``given`` statement local namespace clause)


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

The Devil is in the Details
---------------------------

This section is for ideas that I actually like and think should be added,
but need a champion that's willing to dig into them and flush out the
details through the PEP process.

* `Bytes and Text Transform API`_ (but also see the :ref`codec-pipelines`
  API concept)

.. _Bytes and Text Transform API: http://bugs.python.org/issue7475

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

