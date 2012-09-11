Core Packaging API
==================

.. note::
   To provide feedback on this draft, use the `issue tracker`_ or just send
   me an email.

.. _issue tracker: https://bitbucket.org/ncoghlan/misc/issues?status=new&status=open

The ``packaging`` module (based on the ``distutils2`` project) was slated for
inclusion in Python 3.3. However, it was ultimately removed, as the lead
developers of the project felt it was not yet sufficiently mature.

However, while they were ultimately cut along with the rest of the package,
four submodules almost made it in. Those modules will be the first to make
their reappearance in 3.4

I'm not one of the distutils2 maintainers, but I decided to start writing
this PEP anyway to try to ensure we don't get a repeat of what happened with
3.3. I hope that by setting some clear targets to aim for short of "fix
Python packaging", that identify specific subsets of the distutils2 feature
set that can be added, it will make it easier for the distutils2 project
leads to decide priorities.


Scope
-----

This spec is specifically about the four modules that almost made it into
Python 3.3:

* ``packaging.version`` — Version number classes
* ``packaging.metadata`` — Metadata handling
* ``packaging.markers`` — Environment markers
* ``packaging.database`` — Database of installed distributions

It is expected that some ``distutils2`` utility modules (or parts thereof)
will also need to be incorporated in order for the above modules to be added
to the standard library.

For background, see `this thread`_. (Note that Daniel Holth has since
started working on a standard binary distribution format in the ``wheel``
project, written up as :pep:`425`)

.. _this thread: http://mail.python.org/pipermail/python-dev/2012-June/120488.html


Requirements
------------

The reason these modules failed to be included in Python 3.3 is because the
lead developer indicated that he didn't believe even they were ready for full
standardisation.

