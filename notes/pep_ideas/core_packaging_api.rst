My Current Views on Python Packaging
====================================

.. note::
   To provide feedback on this draft, use the `issue tracker`_ or just send
   me an email.

.. _issue tracker: https://bitbucket.org/ncoghlan/misc/issues?status=new&status=open

The ``packaging`` module (based on the ``distutils2`` project) was slated for
inclusion in Python 3.3. However, it was ultimately removed, as the lead
developers of the project felt it was not yet sufficiently mature.

However, while they were ultimately cut along with the rest of the package,
four submodules almost made it in. Those modules will be the first to make
their reappearance in 3.4, once the PEPs they implement have been tweaked to
close some of the identified holes.

The project focused on identifying the functionality that is sufficiently
mature for stdlib inclusion is ``distlib``.

.. note::

    The grand scheme below *doesn't* replace adding these core modules back
    in to the standard library. The legacy formats will be around for a good
    while yet (assuming they ever get replaced at all) and solid
    infrastructure for reading and writing them will be essential. See the
    section discussing `Near Term`_ efforts.

I'm not one of the distutils2 or distlib maintainers, but I decided to start
writing this up anyway to help ensure we don't get a repeat of what happened
with 3.3. I also want to make sure that any new packaging system doesn't end
up falling into the same trap of implementation defined behaviour that is
such a pain with the status quo.


Background
----------

(This is painted in very broad strokes, both because the details don't
really matter, and also because I don't want to go double check
everything I would have to in order to get the details right)

Python's packaging history largely starts with the inclusion of the
``distutils`` project into the standard library. This system was
really built to handle distribution of source modules and simple
C extensions, but ended up being pushed well beyond that task.

Another key piece of the puzzle was the creation of the Python Package
Index to serve as a central repository for Python packages that could
be shared by the entire community, without being coupled to any particular
operating system or platform specific packaging format.

One notable enhancement was Phillip Eby's ``setuptools``, which became popular
after he created it as part of the work he was doing for OSAF. This
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
complications on top. This limited the adoption of setuptools to those
users that *really* needed the features it provided. Many other parts of
the Python community didn't see the necessity, and instead rejected
setuptools as an opaque blob of magic that they didn't want anywhere near
their systems. setuptools has also suffered PR problems due to its close
association with ``easy_install``, the default behaviour of which violated
many users and system administrators assumptions about how a language
specific packaging tool should behave. The more recent ``pip`` project builds
on the setuptools defined metadata and provides similar functionality to
``easy_install``, but does so in a way that is far more palatable to a wider
range of Python users.

The setuptools project inherited many of the distutils documentation
problems, in particular the lack of specification of file formats. Even
today, you won't find a clear specification of the expected contents of
a Python ``sdist`` archive.

The way setuptools was written also coupled it tightly to internal details
of the standard library's distutils package. This coupling has effectively
frozen feature development within distutils itself, as changes have a
very high risk of breaking previous versions of setuptools.

The ``distribute`` project was created as a fork of setuptools that aims to
act as a drop-in replacement for setuptools, with much clearer documentation
and a broader developer base. However, this project is limited in its
ability to move away from any undesirable default behaviours in setuptools.

These issues led to the creation of the distutils2 project, as a way to
start migrating to an updated packaging infrastructure. As the core
development team largely wasn't concerned about cross platform packaging
issues, the burden of guiding the packaging improvement effort landed on a
small number of heads (mostly Tarek Ziadé and Éric Araujo, and they became
core developers in large part *because* they were working on packaging and
the rest of us were just happy that someone else had volunteered to handle
the job).

At the PyCon 2011 language summit, the decision was made to adopt distutils2
wholesale into Python 3.3 as the ``packaging`` package. At `Éric Araujo's
recommendation`_, that decision was reversed late in the Python 3.3 release
cycle, as he felt the distutils2 code, and the PEPs it was based on simply
weren't ready as the systematic fix that was needed to convince the
community as a whole to migrate to the new packaging infrastructure.

In the ensuing discussion, many good points were raised. This essay started
as my attempt to take a step back and *clearly define the problem that needs
to be solved*. Past efforts have tried to work from a goal statement that
consisted of little more than "fix Python packaging", and we can be
confident that without a clearer understanding of the problems with the
status quo, we aren't going to be able to devise a path forward that
works for all of these groups:

* current distutils users
* current satisfied setuptools/distribute users
* users that are not happy with either setuptools *or* distutils

In practice, the aspects of the problem that caught my interest turned out
to be a few steps beyond the aspects that people are working on *right now*.
However, I hope it will still prove interesting to at least some folks :)

.. _Éric Araujo's recommendation: http://mail.python.org/pipermail/python-dev/2012-June/120430.html


My Position
-----------

I've been trying to ignore this problem for years. Since working at Red Hat,
however, I've been having to deal with the impedance mismatch between RPM
and Python packaging. As valiant as the efforts of the distutils2 folks have
been, I see their proposals as being to replace a system that sucks with a
system that is significantly better in a few specific ways, but still sucks
a whole lot.

If the option is the status quo, or upgrading to something that is
different-but-still-awful-in-many-ways, then I'd almost prefer to just go
back to the 2.5 era plan of just adopting setuptools and then trying to
refactor the implementation over time once it was in the same code base as
distutils. (Relax, I said *almost*)

However, I think it's possible for us to be more ambitious and create
an alternative approach that *doesn't suck* (at least as far as any
packaging system can not suck).


Near Term
---------

Others are working more directly on some key near term improvements. The
``packaging``/``distutils2`` effort has split off a separate project
called ``distlib``. The idea of ``distlib`` is for it to be the place
where core APIs for manipulating the new metadata can go *as the stabilise*.
This is in contrast to ``distutils2`` which includes a lot of legacy
cruft from ``distutils`` which it had been attempting to refactor in place.

Daniel Holth is working on a cross platform binary distribution format called
``wheel``. This is already available on PyPI, with the draft format
specification being documented in PEP 427. This effort is supported by a
couple of other PEPs, most notably an update of the distribution metadata
format to 1.3. The key additions in the new version of the metadata are
"Setup-Requires-Dist" for build time dependencies, as well as a new
extension mechanism allowing custom metadata to be included in the main
metadata file without confusing distribution tools.

This is a critical step, as it will finally allow the build systems to be
decoupled from the installation systems - if ``pip`` can get its hands on
a ``wheel`` file for a project, it will be possible to install it, even
if it uses some arcane build tools that only run on specific systems.

Other steps that are needed are a clearly defined scope and interface for
the ``pysetup`` command line tool that should hopefully be added to the
standard installation in 3.4, as well as a ``distlib`` API to simplify
interacting with PyPI. I'm not sure if those are being actively worked
on at the moment - best to check with the ``distlib`` folks.

Replacing the complex distutils "command" system with something simpler is
also highly desirable. The ``wheel`` format provides the opportunity to
redefine Python's build step as "given an sdist archive, or equivalent
directory layout, produce a wheel archive, or equivalent directory
layout".

The concepts described in this document are *not* an alternative to those
efforts, they're either a follow on project or just background on where
those projects fit into the larger scope of distribution in general.


Longer Term
-----------

I'm personally more interested in the *long* term. One of the problems with
the current distribution mechanisms in Python is that we have an import
system that does everything it can to be filesystem agnostic, but a
packaging and distribution system that is *only defined* for files and
directories on disk. (Go read PEP 376 and ask yourself how you're meant
to publish metadata for a distribution installed inside a zipfile or
loaded from a database via an import hook).

So, I'd like to eventually *abstract away* the filesystem for the
distribution metadata, just as we have already done for the import system
(starting with the introduction of import hooks in PEP 302, now largely
completed in 3.3 with the migration to ``importlib`` as the machinery
powering the import statement and the rest of the import system).

The key step needed for *that* transition is to move away from a *file*
based metadata format to a *data structure* based metadata format. This
is the same transition that happened for configuration of the logging
system when PEP 391 introduced a dictionary-based configuration format
as an alternative to the existing ``ConfigParser`` based format.

I'm also interested in making it easier for *non-Python* tools to process
Python distribution metadata, which is another place where a data structure
based metadata format can help: serialisation to standard formats (such
as JSON) makes it easy for that data to be imported into other tools.


The Phases of Distribution
--------------------------

One component severely lacking in the status quo is a well-defined model
of the phases of distribution. A packaging system needs to be able handle
several distinct phases, especially the transitions between them. For
Python's purposes, these phases are:

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
poorly defined data interchange formats.

distutils isn't much better, since it is still an unholy combination of a
build system *and* a packaging system. Even RPM doesn't go that far: it's
"build system" is just the ability to run a shell script that invokes
your *real* build system.


Assumptions
-----------

This essay assumes that a ``pysetup`` script will make its way back into
the core Python distribution in order to handle tasks that currently
rely on direct execution of setup.py files, and that the metadata previously
supplied by calling ``setup()`` will instead be stored in a static metadata
file.


Working In Development
----------------------

setuptools offers the ``./setup.py develop`` command. This hacks a \*.pth file
created by setuptools in order to add additional directories to the Python
path. Personally, I've always just created symlinks from my working
directory, to whatever extra directories I needed, but it's also a long
time since I needed to care about developing on Windows (outside CPython).

A cleaner way to implement this feature as ``pysetup develop`` would be to
simply add a ``pypi-dist-name.pth`` file with the absolute path of the
current directory to site-packages when ``pysetup develop`` is run from a
directory contain a distribution metadata file (respecting any defined
virtual environment).


Creating a Source Archive
-------------------------

With distutils/setuptools, source archive creation is handled by calling
``./setup.py sdist``. The source archive format is not well defined (beyond
"the format produced by distutils when asked to creat an sdist file"), but
actually consists of a top level ``PKG-INFO`` file as well as all the source
files that will be needed to build and install the distribution.

The ``PKG-INFO`` format is defined in various PEPs. The latest draft is
PEP 426 (v1.3), while the latest approved version is PEP 345 (v1.2, supported
by pip, distribute and PyPI, but not setuptools or distutils) and the latest
version supported by distutils is PEP 314 (v1.1 - supported since 2.5). For
the purposes of this essay, assume I'm talking about v1.3 metadata.

The way this step currently works is that the setup.py file will contain
a call to setup(). It is this call which will actually generate the metadata
file. The MANIFEST.in file is used to control which files are included in
the source distribution. distutils *also* looks for information in a
``setup.cfg`` file, which will override the details of the call to
``setup()``. You can also override many of the settings via command line
options.

distutils2 proposes to change this to rely solely on "setup.cfg", which
is then parsed by a ``pysetup sdist`` call to create a PKG-INFO file for
inclusion in the source archive. The setup.cfg file requires some strange
contortions in order to properly represent structured data. I believe
MANIFEST.in is still used to select files.

By contrast, packaging systems like RPM use a single specification file
for metadata throughout the entire packaging chain. None of the
packaging steps alter this file - they just pass it along faithfully.

.. note::

    I'm currently rewriting this doc, everything below this note hasn't
    been updated yet.

I believe RPM offers a better source of inspiration here: we really want a
single metadata definition that can be passed faithfully through all the
steps of the packaging process, with different phases looking at different
subsets of the metadata. The only file that should be unique to the
"create a source archive" step is MANIFEST.in.

With my encouragement, Donald Stufft is working on a JSON based alternative
to both setup.cfg and PKG-INFO. The file will be largely modelled on
PKG-INFO, but will also include those setup.cfg elements that never make
their way into PKG-INFO in the normal case (e.g. the info that used to be
passed to ``setup()`` as the ``package_data`` and ``data_files`` arguments).
Automated conversion both to and from the legacy formats will be supported,
and projects would easily be able to maintain backwards compatibility by
shipping both PKG-INFO and the new JSON format in their source archives.
Removing the need to parse and emit complex, custom file formats should
remove some of the drudgery associated with building interoperable Python
packaging tools. Using a standard format with full structured data support
also makes it easier to define a validation schema for the metadata
definition.

Unlike the current metadata format (even the updated version proposed in
:pep:`426`), this JSON based format cleanly supports optional extensions. For
example, the not-yet-standardised "entry point" metadata from setuptools can
be encoded simply as::

    "Extensions":
      {
        "setuptools":
          {
            "entry_points":
                <current entry points argument syntax>
          }
      }

To embed such an extension in the current metadata format would be difficult,
as the RFC 822 inspired syntax does not allow for self-describing structured
data. Instead, structured data support must be predefined for each field
that needs it.

``pysetup sdist`` would:

* choose the files to include based on MANIFEST, MANIFEST.in and the JSON metadata
* generate a legacy PKG-INFO from the JSON metadata
* bundle everything up into a source archive

The general idea is that *humans* could use whatever metadata format they
want during development, but they *must* turn it into the machine readable
JSON format for the new packaging infrastructure to handle the rest of the
process.


Building A Binary Distribution
------------------------------

(Note: disentangling the build mess is going to be one of the hardest
problems. My goal is to have the standard library do as *little as possible*
and cede this field to third party build tools. The details below are a
statement of intent, moreso than a definite plan).

Daniel Holth is working on a cross-platform binary distribution platform
format called ``wheel``. With the increasing usage of Python for scientific
tools with complex build requirements, as well as the increased use of
virtual environments, a versatile platform neutral binary packaging format
is essential to providing a good end user experience.

I propose that the standard library get out of the build system business
almost entirely (aside from retaining the existing distutils infrastructure
for backwards compatibility purposes). Instead, distributions which require a
build system should simply identify that as a build dependency (which the
updated metadata format will support). This area is simply not ripe for
(re)standardisation.

Under this approach, the standard "build system" would consist solely of
the full name of a Python callable in a new metadata attribute. The
signature would be as follows::

    def build(bdist_format, metadata):
        # bdist_format is the kind of output file requested
        # metadata is the parsed metadata for the package
        # return value is the path of a directory using the "WHEEL" layout

If no build format was specified, then Python would fall back to checking for
a setup.py file and invoking that.

A new hook would also be provided to allow distutils to be invoked as the
build machinery without requiring a setup.py file.

A "distutils" extension section in the metadata would allow the provision of
additional options for the individual commands.

Other build tools would be expected to follow a similar model: their build
hook named in the metadata, and any configuration options needed stored
as metadata extensions. Third party build tools like ``bento`` would also
need to be listed as build requirements.

Invocation would be ``pysetup bdist_<whatever>``. ``pysetup bdist`` would
always default to ``pysetup bdist_wheel``.


Installation
------------

This would basically follow the featureset of ``pip`` and the general
philosophy of the database format described in PEP 376, except that the
master copy of the metadata for each distribution would be JSON instead.

One key advantage over the current distutils2 proposal is that, as
described above, a JSON configuration format makes it *much* easier to
include optional enhancements and extensions, like setuptools entry points,
in ways that the rest of the tool chain will respect and pass along without
error. Conventions used by particular groups can thus be controlled by
those groups without requiring python-dev involvement. (:pep:`426` proposes
a subset of this within the confines of the existing PKG-INFO format, but
this is very limiting. It's not obvious how to express entry points as an
extension, for example, since the argument syntax can't be used directly
the way it can with JSON. You can do it as a separate file, but that's
a lot harder to parse and present in a generic fashion)


Execution
---------

Again, the extensibility of the metadata makes it a lot easier to pass
along interesting info without requiring standardisation. PyPI distribution
names are used for namespacing, so conflicts should not occur.
