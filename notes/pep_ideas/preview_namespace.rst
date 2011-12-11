Standard Library Preview Namespace
==================================

python-ideas: http://mail.python.org/pipermail/python-ideas/2011-August/011317.html

This isn't originally my idea (that honor goes to `Dj Gilcrease`_), it's just
something I think would be really valuable and that I have some definite ideas
about.


The Namespace
-------------

Red Hat have a concept of "tech previews" that they use for features that they
don't believe are fully mature yet, but that they want to provide to customers
in order to gather early feedback.

I think ``__preview__`` would be a great term for this namespace.


The Benefits for python-dev
---------------------------

Currently, we're *really* reluctant to add new interfaces to the standard
library. This is because as soon as they're published in a release, API
design mistakes get locked in due to backwards compatibility concerns.

By gating all major API additions through the preview namespace for at least
one release, we get one full release cycle of community feedback before we
lock in the APIs with our standard backwards compatibility guarantee.

This is similar to the way the ``sets`` module was used to gather broad
API feedback before the final API of the ``set`` and ``frozenset`` builtins
was determined.

We can also start integrating preview modules in with the rest of the
standard library, so long as we make it clear to packagers that the preview
modules should *not* be considered optional. The only difference between
preview APIs and the rest of the standard library is that preview APIs are
explicitly exempted from the usual backwards compatibility guarantees)


The Benefits for End Users
--------------------------

For end users, the key benefit lies in ensuring that anything in the preview
namespace is clearly under python-dev's aegis from at least the following
perspectives:

* licensing (i.e. redistributed by the PSF under a Contributor Licensing
  Agreement)
* testing (i.e. the module test suites are run on the python.org buildbot
  fleet and results published via http://www.python.org/dev/buildbot)
* issue management (i.e. bugs and feature requests are handled on
  http://bugs.python.org)
* source control (i.e. the master repository for the software is published
  on http://hg.python.org)

Those are the things that will allow the preview modules to be used under
existing legal approvals that allow the use of Python itself (e.g. in a
corporate or governmental environment).


The Rules
---------

New modules added to the standard library spend at least one release in the
``__preview__`` namespace (unless they are using a largely pre-defined API,
such as the new ``lzma`` module).

API updates to existing modules may also be passed through this namespace at
the developer's discretion. In such cases, the module in the preview
namespace should use ``from original import *`` so that users never need to
include both versions.


The Candidates
--------------

For Python 3.3, there are a number of clear current candidates:

* regex
* daemon (`PEP 3143`_)
* ipaddr (`PEP 3144`_)

Other possible future use cases include such things as:

* improved HTTP modules (e.g. requests)
* HTML 5 parsing support (e.g. html5lib)
* improved URL/URI/IRI parsing
* a standard image API (`PEP 368`_)
* encapsulation of the import state (`PEP 368`_)
* standard event loop API (`PEP 3153`_)
* a binary version of WSGI for Python 3 (e.g. `PEP 444`_)
* generic function support (e.g. `simplegeneric`_)

.. _Dj Gilcrease: http://mail.python.org/pipermail/python-ideas/2011-August/011278.html
.. _PEP 3143: http://www.python.org/dev/peps/pep-3143/
.. _PEP 3144: http://www.python.org/dev/peps/pep-3144/
.. _PEP 368: http://www.python.org/dev/peps/pep-368/
.. _PEP 406: http://www.python.org/dev/peps/pep-406/
.. _PEP 3153: http://www.python.org/dev/peps/pep-3153/
.. _PEP 444: http://www.python.org/dev/peps/pep-444/
.. _simplegeneric: http://bugs.python.org/issue5135