Standard Library Preview Namespace
==================================

python-ideas: http://mail.python.org/pipermail/python-ideas/2011-August/011317.html

This isn't originally my idea (that honor goes to `Dj Gilcrease`_), it's just
something I think would be really valuable and that I have some definite ideas
about.

Guido's Verdict
---------------

Eli Bendersky ran with this idea and wrote it up as `PEP 408`_. As you can
see if you click on that link, Guido rejected the PEP in favour of slightly
relaxing the rules for stdlib inclusion: if we're not 100% sure of an
addition, even after it has been battle-tested and received widespread
approval on PyPI, we now have the option to add it anyway, with a
documented warning that the inclusion of the library is provisional. It
will remain at least for that version, but there's a slim chance it will be
removed, or experience backwards incompatible API tweaks in the next feature
release. (The most likely outcome, however, is that it will remain unchanged
for the next release and simply lose the "provisional" tag)

Guido's chosen way forward is actually very similar to the way Google now
provides experimental modules on App Engine under their final names with an
"Experimental!" tag on their documentation (after an earlier failed
experiment with a dedicated "labs" namespace). It's also virtually identical
to the way that Red Hat provides some product features as `tech previews`_
(i.e. without being covered by the usual support guarantees).

In all cases the intended plan is that the incorporated module or feature
will, in fact, end up satisfying the normal backwards compatibility
guidelines. The documented warning just gives us an out where we have the
*option* of making a backwards incompatible change if we deemed it necessary.

The new policy was written up as `PEP 411`_.

.. _PEP 408: http://www.python.org/dev/peps/pep-0408/
.. _PEP 411: http://www.python.org/dev/peps/pep-0411/
.. _tech previews: https://access.redhat.com/support/offerings/techpreview/


The Namespace
-------------

Red Hat have a concept of "tech previews" that they use for features that they
don't believe are fully mature yet, but that they want to provide to customers
in order to gather early feedback.

I think ``__preview__`` would be a great term for this namespace.


Why not __future__?
-------------------

Python already has a "forward-looking" namespace in the form of the
``__future__`` module, so it's reasonable to ask why that can't be re-used
for this new purpose.

There are two reasons why doing so not appropriate:

1. The ``__future__`` module is actually linked to a separate compiler
directives feature that can actually *change* the way the Python interpreter
compiles a module. We don't want that for the preview namespace - we just
want an ordinary Python package.

2. The ``__future__`` module comes with an express promise that names will
be maintained in perpetuity, long after the associated features have become
the compiler's default behaviour. Again, this is precisely the *opposite* of
what is intended for the preview namespace - it is almost certain that all
names added to the preview will be removed at some point, most likely due to
their being moved to a permanent home in the standard library, but also
potentially due to their being reverted to third party package status (if
community feedback suggests the proposed addition is irredeemably broken).


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
standard library early, so long as we make it clear to packagers that the
preview modules should *not* be considered optional. The only difference
between preview APIs and the rest of the standard library is that preview
APIs are explicitly exempted from the usual backwards compatibility
guarantees)


The Benefits for End Users
--------------------------

For future end users, the broadest benefit lies in a better "out-of-the-box"
experience - rather than being told "oh, the standard library tools for task
X are horrible, download this 3rd party library instead", those superior
tools are more likely to be just be an import away.

For environments where developers are required to conduct due diligence on
their upstream dependencies (severely harming the cost-effectiveness of, or
even ruling out entirely, much of the material on PyPI), the key benefit lies
in ensuring that anything in the preview namespace is clearly under
python-dev's aegis from at least the following perspectives:

* licensing (i.e. redistributed by the PSF under a Contributor Licensing
  Agreement)
* testing (i.e. the module test suites are run on the python.org buildbot
  fleet and results published via http://www.python.org/dev/buildbot)
* issue management (i.e. bugs and feature requests are handled on
  http://bugs.python.org)
* source control (i.e. the master repository for the software is published
  on http://hg.python.org)

Those are the things that should allow the preview modules to be used under
any existing legal approvals that allow the use of Python itself (e.g. in a
corporate or governmental environment).


The Rules
---------

New modules added to the standard library spend at least one release in the
``__preview__`` namespace (unless they are using a largely pre-defined API,
such as the new ``lzma`` module, which generally follows the API of the
existing :mod:`bz2` module).

API updates to existing modules may also be passed through this namespace at
the developer's discretion. In such cases, the module in the preview
namespace should use ``from original import *`` so that users never need to
include both versions.

Adding this preview namespace doesn't mean that the floodgates suddenly open
for the addition of arbitrary modules and packages to the standard library.
All of the existing criteria regarding "best of breed" projects, sufficient
API stability and general project maturity to cope with an 18 month release
cycle, etc would still apply. Also, as Ethan Furman once put it, the standard
library philosophy is "batteries included", not "nuclear reactors included".
Some projects are simply too big and too complicated to become part of the
standard library - in such cases, it is better for the standard library to
define standard interfaces that allow third party projects to interoperate
effectively, rather than trying to do everything itself (e.g. :mod:`wsgiref`,
:func:`memoryview`).

All the preview namespace is intended to do is lower the risk of locking in
minor API design mistakes for extended periods of time. Currently, this
concern can block new additions, even when the python-dev consensus it that
a particular addition is a good idea in principle.


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