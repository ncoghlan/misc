Python Concepts
===============

Years ago (around the Python 2.5 time frame) I wrote a draft manuscript for
a `Python User's Reference`_ that aimed at providing a middle ground between
the tutorial and the full language reference. The idea was to cover
everything that was included in the language reference, but in a way that
was designed to help Python developers understand what the interpreter was
doing on their behalf, rather than being aimed at developers trying to
produce a compliant interpreter implementation.

That book deal never went anywhere, so I asked for the copyright on the
manuscript to be returned, and donated the draft to the PSF. Converting the
ODF files to reStructuredText has been an idle thought ever since, but my
motivation to do so has dropped ever lower as the contents of the manuscript
become increasingly out of date.

So, instead, this page will host an ad hoc series of articles that dive deep
into some esoteric element of the Python language definition, and attempt to
explain it in ways that may be more intuitive than the official version.

.. _Python User's Reference:
   http://svn.python.org/view/sandbox/trunk/userref/

.. toctree::
   :maxdepth: 2

   import_traps.rst
   break_else.rst

