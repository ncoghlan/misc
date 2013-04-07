Python Language Summit
======================

Note: while a few procedural decisions were made (such as the Discussions-To:
header becoming more significant for PEPs), this was more an information
sharing session than it was about making decisions on any particular topic.

State of PyPy
-------------

Armin Rigo and Maciej Fijalkowski

* PyPy 2.0 not far away
* PyPy/RPython split in progress. Separated directories in the main PyPy
  repo, will move to separate repos some time post-2.0 (requires a lot of
  fixes to related tools)
* ARM support in progress, will chat to Trent regarding better access to ARM
  machines through Snakebite
* making good progress on Py3k support


State of Jython
---------------

Phillip Jenvey

* Jython 2.7b1 released last month
* Will look at 3.3 support after 2.7 is released
* Java 7 "invoke dynamic" support doesn't actually work yet (JRuby tried it),
  but once it is working and Jython has been updated to use it, then it
  should make for substantial performance improvements


State of IronPython
-------------------

Jeff Hardy

* Already supports 2.7
* Jeff's made some attempts at Python 3 support, hopes to take another
  look this year
* Not many contributors, definitely welcome more
* Now Apache licensed on Github (shared repo with IronRuby)


Packaging Eco-System
--------------------

Me

* Previous effort involved a lot of good work, but various factors
  have limited adoption in practice
* Current efforts are focused on decoupling the build toolchains from the
  installation tools
* Will be giving the "Discussions-To" header in PEPs more significance: the
  announcement of acceptance of a PEP with that set will happen on the named
  list and copies will not be sent to python-dev.
* PEPs involving standard library changes will still have to happen on
  python-dev
* Need better documentation for the overall packaging and distribution tools
  ecosystem. I've started such a thing, but at the moment it is just a
  forlorn issue sitting alone in a "python-meta-packaging" repo I created
  under the PSF's BitBucket account.


XML and Security
----------------

Brett Cannon

* Many security issues inherent in the XML spec.
* Hard to decide how to update the standard library appropriately
* "Secure-by-default" is highly desirable, but some things are inherently
  dangerous (e.g. pickle, XML)
* May settle for readily available "safer XML parsing" config options that
  frameworks may choose to enable by default
* Also some communication issues with being clear on what is currenty
  blocking CPython point releases



Tulip and enhanced async programming support in the standard library
--------------------------------------------------------------------

Guido van Rossum

* PEP 380 almost made it into 2.7. Integration issues (such as the lack of
  unit tests and docs) and the language moratorium meant it ended up being
  delayed until 3.3
* Non-blocking socket support and asyncore exist, but not a great foundation
  for robust async IO infrastructure
* Twisted and Tornado show how event based async IO can be succesful in
  Python
* Guido still doesn't like callback based programming :)
* Aim to create a universal event loop API for Tornado/Twisted/et al
  to interoperate
* Also aim to make it possible to write yield-from based async code
* Read PEP 3156 and related discussions, we mostly just rehashed those
  for the benefit of those that hadn't been following along through the
  many, many threads on python-ideas :)


Parallelizing the Python Interpreter
------------------------------------

Trent Nelson

* Allow CPython internals to be executed from multiple threads
* Minimise required changes
* Initial attempt on hg.python.org/trent (px branch)
* Only works on Vista+ (relies heavily on Windows features, Trent has ideas
  on how to adapt it to \*nix)
* Wants to get it working as a proof of concept first, then clean up and add
  \*nix based solution
* May end up as a Stackless style persistent fork/derived implementation for
  a long while
* Example of a CPU-bound task based on tulip style async API, able to exploit
  all cores
* GIL still present, no fine-grained locks, no STM
* Intercept "thread-sensitive calls" - anything the GIL protects. (refcounts,
  object allocator, free lists, interpreter globals, etc)
* "Normal" threads behave as they do now
* Declared "parallel threads" do something different
* Low overhead then becomes about detecting whether or not you're in a
  parallel thread *really* fast.
* Windows and POSIX both offer ways to detect thread identity based on a
  single memory read
* Parallel threads only incref/decref when the parallel context is
  created/destroyed, so it is possible to cope with the fact that the main
  thread is effectively ignoring any synchronisation mechanisms
* Main thread *stops* while the parallel threads are running, so it can't
  steal things out from underneath the parallel threads
* Wraps objects with async-protected equivalents
* Ultimately, current version is highly experimental, and it's not yet clear
  if it can be made sufficiently robust to be useful in general.

(There are some promising notions here that may fit with some vague ideas
I've had regarding subinterpreters, but there are a lot of real problems
with the current approach, especially relating to references to mutable
containers that are modified after the parallel context starts. May still be
worth pursuing for the benefif of platforms where multiple processes are a
significant problem for performance especially memory usage. I suggested
Trent look into subinterpreters and the Rust memory model for ways this
could be hardened against the many possible segfault inducing behaviours
in the current imlementation)


Snakebite
---------

Trent Nelson

* Set up to provide interesting architectures and OSes for open source
  projects to test against
* Currently heavily reliant on Trent's time, interested in exploring ways
  to make it more open to external contributions (donate to PSF?)
* AIX, HP-UX, still red on CPython buildbots, some others are only green\
  due to extensive environment setup to get CPython building properly
* Trent is interested in finding ways to make this more useful to the
  community
* Perhaps set up databases for easier database testing?
* Ad hoc BuildBot farms for testing experimental forks?
* Currently pre-built machines on bare metal (mostly more esoteric OSes and
  architectures)


Argument Clinic
---------------

Larry Hastings, Nick Coghlan

* Introspection on builtin and extension functions is currently close to
  useless
* Builtin and extension functions are already too hard to write, adding
  signature data as well isn't a reasonable option
* Solution: add an in-place DSL that generates in-place C to be checked in.
* PEPs 436 (Larry) and 437 (Stefan Krah) are competing flavours of the DSL
* Both PEPs agree on the general concept of adding a preprocessor step to
  reduce the complications involved in adding and updating builtin and
  extension module functions and methods
* Both PEPs also agree on checking the *preprocessed* modules with both the
  input and generated output into source control, so the custom preprocessor
  isn't needed to build Python from a source checkout
* Stefan's PEP pushes for a more Python-inspired syntax for the signature
  definition itself, whereas Larry's PEP is more Javadoc inspired (with
  fewer @ symbols and more indentation)
* Since the PEPs are in agreement on most points, Larry, Guido and I will
  get together at some point this week to try to thrash out something
  Guido likes in terms of the DSL syntax details


CFFI
----

Alex Gaynor, Armin Rigo, Maciej Fijalkowski

* cffi competes with both ctypes and SWIG (for C only, not C++)
* unlike ctypes, transparent to the JIT on PyPy (and hence much faster)
* generally slightly faster than ctypes on CPython (due to module generation
  step)
* replaces ctypes for ABI access to shared libraries
* provides an easy way to generate C extensions given a subset of the C API
  details (thus replacing some uses of SWIG and Cython)
* Needs some work to clarify the API and more clearly separate the "create
  an extension module" step from the "load from cached extension module"
  step
* Dependencies are pycparser and PLY for the higher level typesafe API,
  libffi for callback handling and the ABI layer of the API (which is just
  as unsafe and prone to segfaults as ctypes)
* If cffi, and hence pycparser and PLY, are added to the stdlib, all 3
  will be public. We may make use of the "provisional API" status.
* Will reconsider proposal once some of the feedback has been addressed, but
  the idea of adding it certainly seems reasonable


Cross-compilation
-----------------

Matthias Klose

(I confess I wasn't really listening to this part, I was playing catch-up
on Stefan Krah's draft argument DSL PEP he sent me shortly before I left
Australia for PyCon US)

* CPython 3.3 and 2.7 both support cross-compilation (e.g. x86_64 to ARM)
* still a few issues in various regards
* looking to propose additional more invasive changes to the build process to potentially make this easier


Test Facilities
---------------

Robert Collins

* stdlib test facilities are focused on in-process testing
* cross-platform and cross-process and parallel testing becoming more
  important
* easier to drop into a debugger (especially a remote debugger!)
* Robert has a stack that can do this for ordinary unittest-based tests
* Michael is interested in evolving unittest itself as needed, but need to
  figure out appropriate things to do


Enums in the standard library
-----------------------------

Barry Warsaw

* Feature set of ``flufl.enum`` is pretty good
* Don't want to implement the superset of all third party enum libraries
* Precedent set by bool is for enums to seamlessly interoperate with integers
* Highly desirable for any stdlib enum solution to be usable as a replacement
  for the constants in the socket and errno libraries without a backwards
  compatibility break
* Guido doesn't want to have 2 similar enum types in the stdlib, and he wants
  one that can be used in socket and errno (he called this behaviour
  ``bdfl.enum``, to contrast with ``flufl.enum``)
* Guido is OK with different enum types comparing equal, and requiring
  explicit type checks to limit an API to accepting only particular enum
  types
* As a proponent of labelled values over any form of enum, Guido's stated
  preference for "enum as labelled int" (following the precedent set by
  bool) actually works for me
* Barry is in favour of bitmask support for flufl.enum anyway, which is the
  other element (other than comparisons) needed for a solid proposal that is
  interoperable with integers
* Guido also made the point that this is a case where "good enough" will
  likely be enough to kill off most third party enums over time


Requests
--------

Larry Hastings

* With Kenneth Reitz declaring a stable API for requests with 1.0, he's
  interested in offering it for stdlib inclusion in 3.4
* chardet and urllib3 vendored dependencies are a concern for
  incorporation, particularly with tulip/PEP 3156 also coming in Python 3.4
* a tulip-backed requests would be much easier to include (as well as a
  validation of tulip's support for writing synchronous front ends to the
  async tulip backend.


Legacy Modules
--------------

Nick Coghlan

* Better indicate deprecated libraries in the table of contents
* Maybe by a separate section in the ToC, or just by appending
  "(deprecated)" to the section titles


Things we didn't cover
----------------------

These didn't get covered because I forgot to put them on the agenda.
I'll probably be chatting to people about them during the week anyway:

* PEP 422 (simple customisation of class creation)
* PEP 432 (CPython interpreter initialization)
* Unicode improvements (change stream encodings, better encoding specification
  in subprocess, restore type agnostic convenience access to the codecs
  module)
