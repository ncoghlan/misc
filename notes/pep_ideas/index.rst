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


Development Philosophy
----------------------

This sections covers my general development philosophy
as it applies to Python and CPython in particular.

.. toctree::
   :maxdepth: 2

   python_users.rst


Archived Articles
-----------------

These are articles that I wrote to help organise my thoughts on a particular
topic, but am not currently actively maintaining:

.. toctree::
   :maxdepth: 2

   core_packaging_api.rst
   async_programming.rst


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
   release_cadence.rst
   codec_pipeline.rst
   strview.rst

