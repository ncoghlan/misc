Incremental Plans to Improve Python Packaging
=============================================

.. note::
   To provide feedback on this essay, use the `issue tracker`_ or the
   DISQUS comments below.

.. _issue tracker: https://bitbucket.org/ncoghlan/misc/issues?status=new&status=open

As of March 2013, the Python packaging ecosystem is currently in a rather
confusing state. If you're starting a new Python project, should you use the
``distutils`` system in the standard library to publish your software? Or
should you use ``setuptools``? If you decide to use ``setuptools``, should
you download the PyPI distribution that is actually *called* ``setuptools``,
or should you download the competing ``distribute`` distribution, which
*also* provides ``setuptools``?

If you're on Linux, it's quite likely your operating system already *comes*
with a pre-installed copy of ``setuptools``. Perhaps you can use that?

The above options all use a Python script called ``setup.py`` to
configure the build and distribution software. You'll see plenty of
essays on the internet decrying this use of an executable configuration
system, and promoting the use of static configuration metadata instead.
So, perhaps the answer is to avoid all of them and use ``distutils2``
(or ```d2to1``), with a ``setup.cfg`` file, or ``bento`` with its
``bento.info`` file instead?

Even on the *installation* side, things are confusing. ``setuptools`` and
``distribute`` both provide a utility called ``easy_install``. Should you
use that? But there are websites telling you that ``easy_install`` is bad
and you should use ``pip`` instead!

Or perhaps everything above is wrong, and you should be using ``hashdist``,
``conda`` or ``zc.buildout`` to create fully defined stacks of dependencies,
including non-Python software?

HALP! MAKE IT STOP!


TL;DR
-----

The current situation *is* messy, especially sinces it makes it hard for
users to find good, clearly authorative, guides to packaging Python
software. While many people are actively working on improving the
situation, it's going to take a while for those improvements to be fully
deployed.

If all you're after is clear, simple advice for right now, today, as of
March 2013, this is as clear as it gets:

* use `distribute`_ to build and package Python distributions and publish
  them to the `Python Package Index`_ (PyPI). The ``setuptools`` and
  ``distribute`` projects are in the process of merging back together,
  but the merger isn't complete yet (I will update this essay as soon
  as that changes).
* use `pip`_ to install Python distributions from PyPI
* use `virtualenv`_ to isolate application specific dependencies from the
  system Python installation
* use `zc.buildout`_ (primarily focused on the web development community)
  or `hashdist`_ and `conda`_ (primarily focused on the scientific community)
  if you want fully intregrated software stacks, without worrying about
  interoperability with platform provided package management systems
* if you're on Linux, the versions of these tools provided as platform
  specific packages should be fine for most purposes, but may be missing
  some of the latest features described on the project websites (and, in
  Fedora's case, calls ``pip`` ``pip-python`` due to a naming conflict with
  an old Perl tool).

.. _distribute: http://pythonhosted.org/distribute/
.. _Python Package Index: https://pypi.python.org
.. _pip: http://www.pip-installer.org/en/latest/
.. _virtualenv: http://www.virtualenv.org/en/1.9.X/
.. _zc.buildout: http://www.buildout.org/
.. _hashdist: http://hashdist.readthedocs.org/en/latest/
.. _conda: http://docs.continuum.io/conda/

Unfortunately, there are a couple of qualifications required on that simple
advice:

* use ``easy_install`` or `zc.buildout`_ if you need to install from the
  binary ``egg`` format, which ``pip`` can't currently handle
* aside from using ``distribute`` over the original ``setuptools`` (again,
  keeping in mind that those two projects are in the process of merging
  back into a single ``setuptools`` project), and ``pip`` over
  ``easy_install`` whenever possible, try to ignore
  the confusing leftovers of slanging matches between developers of
  competing tools, as well as information about upcoming tools that
  are likely still months or years away from being meaningful to anyone
  not directly involved in developing packaging tools

The `Quick Start`_ section of the Hitchhiker's Guide to Packaging provided
by the ``distribute`` team is still a decent introduction to packaging
and distributing software through the Python Package Index. However, the
rest of that guide includes a lot of opinions and plans that don't quite
match up with reality (this is being cleaned up as part of the current
packaging ecosystem improvement efforts).

After the quickstart, your best
options for learning more are likely the `distribute project documentation`_
and the standard library's own guide to :ref:`distutils-index`.

.. _Quick Start: http://guide.python-distribute.org/quickstart.html
.. _distribute project documentation: http://pythonhosted.org/distribute/setuptools.html


A (long) caveat on this essay
-----------------------------

I'm currently the "BDFL-Delegate" for packaging related Python PEPs. It's
important to understand that being a BDFL-Delegate does *not* mean I
automatically get my way - even Guido van Rossum doesn't automatically get his
way in regards to Python, and he's Python's actual Benevolent Dictator for
Life! This is a large part of why we call him a *benevolent* dictator -
most of the time he only needs to invoke his BDFL status to cut short
otherwise interminable arguments where there are several possible answers,
any of which qualifies as "good enough".

Instead, being a BDFL-Delegate means I get to decide when "rough consensus"
has been achieved in relation to such PEPs. I'm trusted to listen to feedback
on PEPs that are being proposed for acceptance (including any where I am both
author and BDFL-Delegate) and exercise good judgement on which criticisms I
think are valid, and need to be addressed before I accept the PEP, and which
criticisms can be safely ignored (or deferred), deeming the contents of the
PEP "good enough" (or at least "good enough for now").

In the case of packaging PEPs, I have identified a core set of projects whose
involvement I consider essential in assessing any proposals (in particular
the updated metadata standard described in :pep:`426`):

* CPython - masters of distutils, the default Python build system
* setuptools - originators of the dominant 3rd party Python build system
* distribute - popular, recommended (and Python 3 compatible) setuptools
  fork (this project and setuptools are in the process of merging back
  together)
* pip - Python installer that addresses many of the design flaws in
  easy_install
* distlib - distribution tools infrastructure, originally part of distutils2
* PyPI - the central index for public Python packages

In addition, there are other projects whose developers provide valuable
additional perspectives:

* zc.buildout - powerful and flexible application deployment manager
* hashdist/conda - a "software stack" management system, tailored towards
  the scientific community, which needs to deal with arcane build
  requirements and a large user community that is interested in software
  solely as a tool rather than in its own right
* distutils2 - alternate build system that replaces setup.py with setup.cfg
  and the last major attempt at bringing order to the Python packaging
  ecosystem
* bento - an experimental alternative build system

Why those projects? A few different reasons:

#. Almost all of the listed projects have representatives that are active on
   distutils-sig and catalog-sig, the primary mailing lists for discussing
   changes that affect the overall Python packaging ecosystem (hashdist/conda
   are currently an exception, but I'm hoping that will change at some point).
#. CPython needs to be involved because support for the new standards should
   be part of the Python 3.4 standard library (just as it was previously
   proposed that distutils2 would be added to the 3.3 standard library).
#. distlib needs to be involved as that is the project to extract the
   core distribution management infrastructure from distutils2 that
   *almost* made it into Python 3.3. It serves as the reference
   implementation for the new metadata format proposed in PEP 426, will
   likely be proposed as the basis of any support for the new formats
   in Python 3.4, and may hopefully be used as part of other distribution
   tools prior to inclusion in the standard library (as a real world
   usability test for the API).
#. PyPI needs to be involved, in order to act as an effective and efficient
   publisher of the richer metadata set
#. Five of the projects (setuptools, distribute, hashdist, distutils2, bento)
   provide build systems that are usable with *current* versions of Python,
   rather than requiring an upgrade to Python 3.4. If a new metadata standard
   is to see widespread adoption, all of them need to be able to generate it.
#. Eight of the projects (setuptools, distribute, pip, zc.buildout,
   conda, distutils2, distlib) provide or rely on dependency resolvers and
   other tools that consume metadata at installation time. If a new metadata
   standard is to see widespread adoption, all of them need to be able to
   correctly retrieve and process that metadata from the package index,
   source and binary archives, as well as the target installation
   environment.
#. Four of the projects (setuptools, distribute, distutils2, distlib)
   provide tools for accessing distribution metadata at runtime. If a new
   metadata standard is to see widespread adoption, all of them need to be
   able to retrieve and process that metadata from the execution environment.
#. Between them, these projects and their derivatives, cover the vast
   majority of the current Python packaging ecosystem. If they collectively
   endorse an updated metadata standard, it has a good chance of succeeding.
   If they reject it, then it really doesn't matter if python-dev nominally
   accepts it (and, in fact, python-dev would be wrong to do so, as we have
   unfortunately learned the hard way).


The Phases of Distribution
--------------------------

One component severely lacking in the status quo is a well-defined model
of the phases of distribution. An overall packaging system needs to be
able to handle several distinct phases, especially the transitions between
them. For Python's purposes, these phases are:

* Development: working with source code in a VCS checkout
* Source Distribution: creating and distributing a source archive
* Building: creating binary files from a source archive
* Binary Distribution: creating and distributing a binary archive
* Installation: installing files from a binary archive onto the target system
* Execution: importing or otherwise running the installed files

The setuptools distribution covers *all six* of those phases. A key goal
of any new packaging system should be to cleanly decouple the phases and make
it easier for developers to choose the right tool for each phase rather
than having one gigantic project that handles everything internally with
poorly defined data interchange formats. Having a single project handle
everything should still be *possible* (at least for backwards compatibility,
even if for no other reason), it just shouldn't be required.

distutils isn't much better, since it is still an unholy combination of a
build system *and* a packaging system. Even RPM doesn't go that far: it's
"build system" is just the ability to run a shell script that invokes
your *real* build system. In many ways, distutils was really intended as
Python's equivalent of ``make`` (or perhaps ``make`` + ``autotools``),
so we're currently in the situation Linux distributions were in before the
creation of dedicated package management utilities like ``apt`` and ``yum``.

It isn't really a specific phase, but it's also desirable for a
meta-packaging system to define a standard mechanism for invoking a
distribution's automated test suite and indicate whether or not it
passed all its tests.


A Meta-Packaging System
~~~~~~~~~~~~~~~~~~~~~~~

My goal for Python 3.4 is to enable a solid *meta-packaging* system,
where we have multiple, cooperating, tools, each covering distinct
phases of distribution. In particular, a project's choice of
build system should NOT affect on end user's choice of installation
program.

In this system, there are a few key points where interoperability
between different tools is needed:

#. For binary distribution, an installation tool should be able to unpack
   and install the contents of the binary archive to the appropriate
   locations, *without* needing to install the build system used to create
   the archive.
#. For source distribution, an installation tool should be able to identify
   the appropriate build tool, download and install it, and then invoke it
   in a standard fashion, *without* needing any knowledge of any particular
   build systems.
#. The central package index needs to accept and publish distribution
   metadata in a format that is easy to consume
#. Installation tools need to store the distribution metadata in a standard
   format so other tools know where to find it and how to read it.

The development phase and the execution phase are the domain of build tools
and runtime support libraries respectively. The interfaces they expose to
end users in those phases are up to the specific tool or library - the
meta-packaging system only cares about the interfaces between the
automated tools.


The ``wheel`` format
--------------------

The binary ``wheel`` format, created by Daniel Holth, and formally
specified in :pep:`427`, is aimed at solving two problems:

* initially, acting as a cache format for ``pip``, allowing that tool to
  avoiding having to rebuild packages from source in each virtual
  environment
* eventually, as build tools gain the ability to publish wheels to PyPI,
  and more projects start to do so, as a way to support distribution of
  Python software that doesn't require the invocation of ``./setup.py
  install`` on the target system

This is a critical step, as it finally allows the build systems to be
systematically decoupled from the installation systems - if ``pip`` can
get its hands on a ``wheel`` file for a project, it will be possible to
install it, even if it uses some arcane build tools that only run on
specific systems.

In many respects, ``wheel`` is a *simpler* format than the setuptools
egg format. It deliberately avoids all of the features of eggs (or, more
accurately, ``easy_install``) which resulted in runtime modifications to
the target environment. Those were the features that people disliked as
being excessively magical, and which limited the popularity of the format.

In two respects, wheel is *more* complex than the egg format. Firstly,
the compatibility tagging scheme used in file names (defined in :pep:`425`)
is more comprehensive, allowing the interpreter implementation and version
to be clearly specified, along with the Python C ABI requirement, and the
underlying platform compatibility.

Secondly, the wheel format allows *multiple* target directories to be
defined, as is supported by the ``distutils`` installation operation. This
allows the format to support correctly spreading files to appropriate
directories on a target system, rather than dropping all files into a
single directory in violation of platform standards (although the wheel
format *does* also support the latter style).


Python distribution metadata v2.0
---------------------------------

My own efforts are currently focused primarily on :pep:`426`, the latest
version of the standard for Python distribution metadata. My aim
with this latest version of the metadata is to address the issues which
prevented widespread adoption of the previous version by:

* deciding on appropriate default behaviour for tools based on the
  experiences of other development language communities
* supporting additional features of setuptools/distribute that were
  missing from the previous version of the standard
* engaging with the distribute and setuptools developers to ensure both
  of those projects (or, as is now more likely, the post-merger
  setuptools) are able to start emitting the new metadata format
  within a reasonable period of time after the standard is accepted
* simplifying backwards compatibility with those same two projects (just one
  after the merger) by adding a recommendation for installation tools to
  correctly generate legacy versions of the metadata that those two projects
  will be able to easily read

I also plan to design this standard to use JSON as the on-disk serialisation
format. There are four reasons for this:

* Over time, the original simple Key:Value format has grown various ad hoc
  extensions to support structured data that doesn't fit the simple key-value
  format. Some fields are "multi-use", some allow embedded environment
  markers, one is a space separated sequence of values. Switching to JSON
  means structured data is supported simply and cleanly, without these ad
  hoc complexities in the parsing rules.
* to completely replace the existing ``./setup.py install`` idiom,
  :pep:`426` is going to need to define a post-install hook, and conversion
  to a more structured format makes it easier to pass the metadata to the
  registered hook
* :pep:`376` currently ignores the existence of import hooks completely: it is
  only correctly defined for Python distributions that are installed to the
  filesystem. Fixing that will require a structured metadata representation
  that can be returned from an appropriate importer method.
* TUF (The Update Framework), is an intriguing approach proposed for adding
  a usable end-to-end security solution to the Python packaging ecosystem.
  One feature of TUF is the ability to embed arbitrary JSON metadata
  describing "targets", which, in Python's case, would generally mean
  source and binary archives for distributions.

Converting the earlier versions of PEP 426 (which still use the old key:value
format as a basis) to a useful platform-neutral JSON compatible metadata
format is actually fairly straightforward, and Daniel Holth already has a
draft implementation of the bdist_wheel distutils command that emits a
preliminary version of it.


Secure metadata distribution
----------------------------

In the wake of the rubygems.org compromise, a topic of particular interest on
catalog-sig is the definition of a reliable, usable, end-to-end security
mechanism that allows end users the option of either trusting PyPI to
maintain the integrity of distributed packages, *or* maintaining their
own subset of trusted developer keys.

While I'm not actively working on this myself, I'm definitely interested
in the topic, and currently favour the concept of adopting
`The Update Framework`_, a general purpose software updating architecture,
designed to protect from a wide variety of known attack vectors on software
distribution systems. I particularly like the fact that TUF may not only
address the end-to-end security problem, but also provide a *far* superior
metadata publication system to that provided by the current incarnation
of the PyPI web service.

A number of the TUF developers are now active on catalog-sig, attempting
to devise an approach to securing the *existing* PyPI metadata, which
may then evolve over time to take advantage of more of TUF's features.

.. _The Update Framework: https://www.updateframework.com/


A Bit of Python Packaging History
---------------------------------

The ``packaging`` module (based on the ``distutils2`` project) was slated for
inclusion in Python 3.3. However, it was ultimately removed, as the lead
developers of the project felt it was not yet sufficiently mature.

Following that decision, the entire approach being taken to enhancing
Python's packaging ecosystem has been in the process of being reassessed.
This essay is part of my own contribution to that reassessment, and the
reasoning described here is the reason I decided to offer to take on the
role of BDFL delegate for any PEPs related to the packaging ecosystem.

This essay also serves as a clear declaration of my vision for how I
think we can avoid repeating the mistakes that limited the overall
effectiveness of the ``distutils2`` effort, and make further improvements
to the Python packaging ecosystem. If this effort is successful, then
improved software distribution utilities should become one of the
flagship features of Python 3.4.


How did we get here?
~~~~~~~~~~~~~~~~~~~~

(This section is painted in fairly broad strokes, both because the details
don't really matter, and also because I don't want to go double check
everything I would have to in order to get the details right)

Python's packaging history largely starts with the inclusion of the
``distutils`` project into the standard library. This system was
really built to handle distribution of source modules and simple
C extensions, but ended up being pushed well beyond that task. I was lucky
enough to meet Greg Ward at PyCon US 2013, and he has posted a great write-up
of the `early history of distutils`__ as part of his post-conference review.

.. __: http://gerg.ca/blog/post/2013/pycon-2013-report/

Another key piece of the puzzle was the creation of the Python Package
Index to serve as a central repository for Python packages that could
be shared by the entire community, without being coupled to any particular
operating system or platform specific packaging format.

One notable enhancement was Phillip Eby's ``setuptools``, which became
popular after he created it as part of the work he was doing for OSAF. This
was subsequently forked to create the ``distribute`` project (like
``setuptools`` itself, the ``distribute`` distribution installs both the
``setuptools`` and ``pkg_resources`` modules on to the target system.

The distutils project suffered from being poorly defined and documented in
many ways. In particular, the phases of distribution were not well documented
and the main "metadata" file used to drive the process was a full-fledged
Python script. This contrasts with other packaging systems, such as RPM,
where the main metadata file may *contain* executable code, but is not
itself executable.

setuptools took that already complicated system, and then layered *more*
complications on top (up to and including monkey-patching the standard
library distutils pacakge when imported). This limited the adoption of
setuptools to those users that *really* needed the features it provided.

Many other parts of the Python community didn't see the necessity, and
instead rejected setuptools as an opaque blob of magic that they didn't
want anywhere near their systems. setuptools has also suffered PR
problems due to its close association with ``easy_install``, the
default behaviour of which violated many users and system administrators
assumptions about how a language specific packaging tool should behave.

The misbehaviour of ``easy_install`` also gave the associated "egg"
binary format a poor reputation that it really didn't deserve (although
that format does have some genuine problems, such as being difficult
to transform into platform specific binary formats, such as RPM, in a
way that complies with typical packaging policies for those platforms,
as well as failing to adequately convey compatibility limitations in
the egg filenames. Both of these deficiencies are addressed at least to
some degree by the recently approved ``wheel`` format).

The setuptools project also inherited many of the distutils documentation
problems, although it does at least provide reasonable documentation for
most of its `file formats`__ (the significant formats on that page are
``requires.txt``, ``entry_points.txt`` and the overall egg format itself).
By contrast, even today, you won't find a clear specification of the
expected contents of a Python ``sdist`` archive.

.. __: http://peak.telecommunity.com/DevCenter/EggFormats

The more recent ``pip`` project builds on the setuptools defined metadata
and provides similar functionality to ``easy_install``, but does so in a
way that is `far more palatable`__ to a wider range of Python users.

.. __: http://www.pip-installer.org/en/1.3.X/other-tools.html#easy-install

The way setuptools was written also coupled it tightly to internal details
of the standard library's distutils package. This coupling, along with
some significant miscommunication between the setuptools and distribute
developers and the core development team, had effectively frozen feature
development within distutils itself for a few years, as a request
to avoid all refactoring changes in maintenance releases managed to
morph into a complete ban on new distutils features for a number of
releases.

The ``distribute`` project was created as a fork of setuptools that aims to
act as a drop-in replacement for setuptools, with much clearer documentation
and a broader developer base. However, this project is limited in its
ability to move away from any undesirable default behaviours in setuptools,
and the naming creates confusion amongst new users.

These issues led to the creation of the ``distutils2`` project, as a way to
start migrating to an updated packaging infrastructure. As the core
development team largely wasn't concerned about cross platform packaging
issues, the burden of guiding the packaging improvement effort landed on a
small number of heads (mostly Tarek Ziadé and Éric Araujo, and they became
core developers in large part *because* they were working on packaging and
the rest of us were just happy that someone else had volunteered to handle
the job).

The ``distutils2`` developers did a lot of things right, including
identifying a core issue with setuptools and easy_install, where behaviour
in certain edge cases (such as attempting to interpret nonsensical version
numbers) resulted in *some* kind of answer (but probably not the answer you
wanted) rather than a clear error. This lead to the creation of a number of
PEPs, most notably :pep:`345` (v1.2 of the metadata standard) and :pep:`386`
(the versioning scheme for metadata v1.2), in an attempt to better define
the expected behaviour in those edge cases. This effort was also responsible
for the creation of the standard installation database format defined in
:pep:`376`, which is what allows ``pip``, unlike ``easy_install``, to
support uninstallation of previously installed distributions.

At the PyCon 2011 language summit, the decision was made to adopt distutils2
wholesale into Python 3.3 as the ``packaging`` package. At `Éric Araujo's
recommendation`_, that decision was reversed late in the Python 3.3 release
cycle, as he felt the distutils2 code, and the PEPs it was based on simply
weren't ready as the systematic fix that was needed to convince the
community as a whole to migrate to the new packaging infrastructure.

.. _Éric Araujo's recommendation: http://mail.python.org/pipermail/python-dev/2012-June/120430.html

In the ensuing discussion, many good points were raised. This essay started
as my attempt to take a step back and *clearly define the problem that needs
to be solved*. Past efforts have tried to work from a goal statement that
consisted of little more than "fix Python packaging", and we can be
confident that without a clearer understanding of the problems with the
status quo, we aren't going to be able to devise a path forward that
works for all of these groups:

* currently satisfied distutils users
* currently satisfied setuptools/distribute users
* users that are not happy with either setuptools *or* distutils

Another significant recent development is that the setuptools and distribute
developers are currently working on merging the two projects back together,
creating a combined setuptools distribution that includes the best aspects
of both of these tools. The merger will also make it easier to make
incremental changes to the default behaviour (especially of
``easy_install``) without abruptly breaking anyone's tools.


My Position
~~~~~~~~~~~

I've been trying to ignore this problem for years. Since working at Red Hat,
however, I've been having to deal with the impedance mismatch between RPM
and Python packaging. As valiant as the efforts of the distutils2 folks have
been, I believe their approach ultimately faltered as it attempted to
tackle both a new interoperability standard between build tools and
installation tools (switching from ``./setup.py install`` to ``pysetup install
project``) *at the same time* as defining a new archiving and build tool
(switching from ``./setup.py sdist`` to ``pysetup sdist project``). This
created a very high barrier to adoption, as the new metadata standards were
only usable after a large number of projects changed their build system.
The latter never happened, and the new version of the metadata standard
never saw significant uptake (as most build tools are still unable to
generate it).

My view now is that it is *necessary* to take it for granted that there
will be multiple build systems in use, and that ``distutils``,
``setuptools`` and ``distribute`` really aren't that bad as *build*
systems. Where they primarily fall down is as installation tools,
through the insidious ``./setup.py install`` command.

That means my focus is on the developers of build tools and installation
tools, to *transparently* migrate to a new metadata format, without
needing to bother end users at all. Most Python developers should be able
to continue to use their existing build systems, and with any luck, the
only observable effect will be improved reliability and consistency of
the installation experience (especially for pre-built binaries on Windows).


