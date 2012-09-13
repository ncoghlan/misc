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
3.3. I also want to make sure that any new packaging system doesn't end up
falling into the same trap of implementation defined behaviour.

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

One notable extension was Phillip Eby's ``setuptools``, which became popular
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
the Python community didn't the see the necessity, and instead rejected
setuptools as an opaque blob of magic that they didn't want anywhere near
their systems. setuptools has also suffered PR problems due to its close
association with ``easy_install``, the default behaviour of which violated
many users and system administrators assumptions about how a language
specific packaging tool should behave. The more recent ``pip`` project builds
on the setuptools defined metadata and provides similar functionality to
easy_install, but does so in a way that is far more palatable to a wider
range of Python users.

The setuptools project inherited many of distutils documentation problems,
in particular the lack of specification of file formats. Even today, you
won't find a clear specification of the expected contents of a Python
``sdist`` archive.

The way setuptools was written also coupled it tightly to internal details
of the standard library's distutils package. This coupling has effectively
frozen feature development within distutils itself, as changes have a
very high risk of breaking previous versions of setuptools.

These issues led to the creation of the distutils2 project, as a way to
start migrating to an updated packaging infrastructure. As the core
development team largely wasn't concerned about cross platform packaging
issues, the burden of guiding the packaging improvement effort landed on a
small number of heads (mostly Tarek Ziadé and Éric Araujo, and they became
core developers in large part *because* they were working on packaging and
the rest of us were just happy that someone else had volunteered to handle
the job).

At the PyCon 2011 language summit, the decision was made to adopt distutils2
wholesale into Python 3.3 as the "packaging" package. At `Éric Araujo's
recommendation`_, that decision was reversed late in the Python 3.3 release
cycle, as he felt the distutils2 code, and the PEPs it was based on simply
weren't ready as the systematic fix that was needed to convince the
community as a whole to migrate to the new packaging infrastructure.

In the ensuing discussion, many good points were raised. This essay is
my attempt to take a step back and *clearly define the problem that needs
to be solved*. Past efforts have tried to work from a goal statement that
consisted of little more than "fix Python packaging", and we can be
confident that without a clearer understanding of the problems with the
status quo, we aren't going to be able to devise a path forward that
works for all of these groups:
    
* current distutils users
* current satisfied setuptools/distribute users
* users that are not happy with either setuptools *or* distutils

.. _Éric Araujo's recommendation: http://mail.python.org/pipermail/python-dev/2012-June/120430.html


My Position
-----------

I've been trying to ignore this problem for years. Since working at Red Hat,
however, I've been having to deal with the impedance mismatch between RPM
and Python packaging. As valiant as the efforts of the distutils2 folks have
been, I see their proposals as being to replace a system that sucks with a
system that is better in a few specific ways, but still sucks a whole lot.

If the option is the status quo, or upgrading to something that is
different-but-still-awful in many ways, then I'd prefer to stick to the
status quo.

However, I think it's possible for us to be more ambitious and create
an alternative approach that *doesn't suck*. If it genuinely doesn't suck,
then it should be easier to encourage adoption, particularly if:

* new metadata can be distributed in parallel with legacy metadata
* new metadata can be parsed and validated without requiring custom tools
* new metadata can easily be parsed from non-Python code
* legacy metadata can be generated from new metadata and vice-versa
* the new system can be plugged into a platform specific packaging system
  at the source archive level in an automated fashion
* the new system can be plugged into a platform specific packaging system
  at the binary archive level in an automated fashion
* dependencies can be mapped to a platform specific packaging system in a
  mostly automated fashion (modulo cases where the distro packagers have
  split a PyPI distribution into multiple system packages)


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
the core Python distribution in order to subsume tasks that currently
rely on direct execution of setup.py files, and that the metadata previously
supplied by calling ``setup()`` will instead be stored in a static metadata
file.


Working In Development
----------------------

setuptools offers the ``./setup.py develop`` command. This hacks a *.pth file
created by setuptools in order to add additional directories to the Python
path. Personally, I've always just created symlinks from my working
directory, to whatever extra directories I needed, but it's also a long
time since I needed to care about developing on Windows (outside CPython).

A cleaner way to implement this feature as ``pysetup develop`` would be to
simple add a ``pypi-dist-name.pth`` file with the absolute path of the
current directory to site-packages when pysetup develop is run from a
directory contain a distribution metadata file (respecting any defined
virtual environment).


Creating a Source Archive
-------------------------

With distutils/setuptools, source archive creation is handled by calling
``./setup.py sdist``. The source archive format is not well defined (beyond
"the format produced by distutils when asked to creat an sdist file"), but
actually consists of a top level ``PKG-INFO`` file as well as all the source
files that will be needed to build and install the distribution.

The ``PKG-INFO`` format is itself not especially well-defined. It's an ad
hoc semi-structured file format. The parsing rules for field content vary
by header, so you can only read it effectively with custom tools like
distutils and setuptools. There are no standard tools that can parse this
file in a manner that is both useful and content neutral.

The way this step currently works is that the setup.py file will contain
a call to setup(). It is this call which will actually generate the metadata
file. The MANIFEST.in file is used to control which files are included in
the source distribution. distutils *also* looks for information in a
``setup.cfg`` file, which will override the details of the call to
``setup()``.

distutils2 proposes to change this to rely solely on "setup.cfg", which
is then parsed by a ``pysetup sdist`` call to create a PKG-INFO file for
inclusion in the source archive. The setup.cfg file requires some strange
contortions in order to properly represent structured data. I believe
MANIFEST.in is still used to select files.

By contrast, with packaging systems like RPM, a single specification file
is used for metadata throughout the entire packaging chain. None of the
packaging steps alter this file - they just pass it along faithfully.

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

I also propose that the standard library get out of the business of
understanding platform specific packaging formats (beyond whatever is
needed to create the Windows and Mac OS X binary installers).

Under this approach, the standard "build system" would consist solely of
the full name of a Python callable in a new metadata attribute. The
signature would be as follows::

    def build(metadata):
        # metadata is the parsed metadata for the package
        # return value is the path of a directory using the "WHEEL" layout

An appropriate hook would be added to allow distutils to be specified as the
build system.

If no build system was specified, then Python would assume that the source
archive consisted solely of pure Python files and static metadata files and
create an appropriate directory layout (essentially, all files dumped in
root directory using layout from sdist).

A new "Commands" section in the metadata would allow the provision of
additional options. As with the build system, the commands system would
permit easy extension by allowing "package" callables to be named::

    def binary_dist(built_dir, metadata):
        # built_dir is the return value
        # metadata is the parsed metadata for the package
        # return value is the path of the built binary package

The standard library would still understand how to create bdist_dumb,
bdist_wininst and bdist_rpm, along with bdist_wheel, without needing
a third party build tool. The metadata file would still allow the
provision of options, however.

Invocation would be ``pysetup bdist_<whatever>``

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
the way it can with JSON)

Execution
---------

Again, the extensibility of the metadata makes it a lot easier to pass
along interesting info without requiring standardisation. PyPI distribution
names are used for namespacing, so conflicts should not occur.
