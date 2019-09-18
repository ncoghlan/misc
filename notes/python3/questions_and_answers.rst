Python 3 Q & A
==============

:Published:    29th June, 2012
:Last Updated: 17th September, 2019

Throughout the long transition to "Python 3 by default" in the Python ecosystem,
the question was occasionally raised as to whether or not the core Python
developers were acting as reasonable stewards of the Python language.

While it largely stopped being a concern after the release of Python 3.5 in
September 2015, it was an entirely appropriate question prior to that, as
Python 3 introduced backwards incompatible changes that more obviously helped
future users of the language than they did current users, so existing users
(especially library and framework developers) were being asked to devote time
and effort to a transition that would cost them more in time and energy in the
near term than it would save them for years to come.

Since I had seen variants of these questions several times over the
years, I started this FAQ as an intermittently updated record of my
thoughts on the topic, with updates generally being prompted by new
iterations of the questions. I gave Sumana Harihareswara co-maintainer
access in September 2019 so she could aid in updating it, but for
simplicity's sake will retain the first-person singular ("I")
throughout. You can see the full history of changes in the `source
repo`_.

The views expressed below are my own. While many of them are shared by
other core developers, and I use "we" in several places where I believe
that to be the case, I don't claim to be writing on the behalf of every
core developer on every point. Several core developers (including Guido)
*have* reviewed and offered comments on this document at various points in
time, and aside from Guido noting that I was incorrect about his initial
motivation in creating Python 3, none of them has raised any objections
to specific points or the document in general.

I am also not writing on behalf of the Python Software Foundation (of which
I am a nominated Fellow) nor on behalf of Red Hat (my current employer).
However, I do use several Red Hat specific examples when discussing
enterprise perception and adoption of the Python platform - effectively
bridging that gap between early adopters and the vast majority of prospective
platform users is kinda what Red Hat specialises in, so I consider them an
important measure of the inroads Python 3 is making into more conservative
development communities.

There were several extensive discussions of the state of the Python 3
transition at PyCon US 2014 in Montreal, starting at the language summit,
and continuing throughout the conference. These helped clarify many of the
remaining points of contention, and resulted in a range of changes to Python
3.5, Python 2.7, and the available tools to support forward migration from
Python 2 to Python 3. These discussions didn't stop, but have rather continued
over the course of Python development, and can be expected to continue
for as long as folks are developing software that either fits into the common
subset of Python 2 & 3, or else are having to maintain software that continues
to run solely under Python 2.

.. note::

   If anyone is interested in writing about these issues in more formal
   media, please get in touch to check if particular answers are still
   accurate. Not only have the updates over the years been intermittent,
   they've also been less than completely comprehensive, so some answers may
   refer out to experiments that ultimately proved unininteresting or
   unsuccessful, or otherwise be out of date.

As with all essays on these pages, feedback is welcome via the
`issue tracker`_ or `Twitter`_.

.. _source repo: https://bitbucket.org/ncoghlan/misc
.. _issue tracker: https://bitbucket.org/ncoghlan/misc/issues
.. _Twitter: https://twitter.com/ncoghlan_dev


TL;DR Version
-------------

* Yes, we know this migration was/is disruptive.
* Yes, we know that some sections of the community had never personally
  experienced the problems with the Python 2 Unicode model that this
  migration was designed to eliminate, or otherwise preferred the closer
  alignment between the Python 2 text model and the POSIX text model.
* Yes, we know that many of those problems had already been solved by
  some sections of the community to their own satisfaction.
* Yes, we know that by attempting to fix these problems in the core Unicode
  model we broke many of the workarounds that had been put in place
  to deal with the limitations of the old model
* Yes, we are trying to ensure there is a smooth migration path from Python
  2 to Python 3 to minimise the inevitable disruption
* Yes, we know some members of the community would have liked the migration to
  move faster and found the "gently, gently, there's no rush" approach of the
  core development team frustrating
* No, we did not do this lightly
* No, we did not see any other way to ensure Python remained a viable
  development platform as developer communities grow in locations
  where English is not the primary spoken language. It should be at least
  possible for users to start learning the basics of Python without having
  to first learn English as a prerequisite (even if English remains a
  requirement for full participation in the global Python and open source
  ecosystems).

It is my perspective that the web and GUI developers have the right idea:
dealing with Unicode text correctly is not optional in the modern world.
In large part, the Python 3 redesign involved taking Unicode handling
principles elaborated in those parts of the community and building them
into the core design of the language.


Why was Python 3 made incompatible with Python 2?
-------------------------------------------------

According to Guido, he initiated the Python 3 project to clean up a variety
of issues with Python 2 where he didn't feel comfortable with fixing them
through the normal deprecation process. This included the removal of classic
classes, changing integer division to automatically promote to a floating
point result (retaining the separate floor division operation) and changing
the core string type to be based on Unicode by default. With a compatibility
break taking place anyway, the case was made to just include some other
changes in that process (like converting print to a function), rather than
going through the full deprecation process within the Python 2 series.

If it had just been about minor cleanups, the transition would likely have
been more straightforward, but also less beneficial. However, the changes
to the text model in Python 3 are one of those ideas that has profoundly
changed the way I think about software, and we receive similar feedback from
many other users that never really understood how Unicode worked in Python 2,
but were able to grasp it far more easily in Python 3. Redesigning the way
the Python builtin types model binary and text data has the ultimate aim of
helping *all* Python applications (including the standard library itself) to
handle Unicode text in a more consistent and reliable fashion (I originally had
"without needing to rely on third party libraries and frameworks" here,
but those are still generally needed to handle system boundaries correctly,
even in Python 3).

.. note::

   For a more complete version of this answer that places it in the wider
   industry context of Unicode adoption, see this article of mine on the Red
   Hat Developer Blog: `The Transition to Multilingual Programming with Python <https://developers.redhat.com/blog/2014/09/09/transition-to-multilingual-programming-python/>`__

   I also gave a presentation on the topic at Python Australia 2015, which is
   available online `here <https://www.youtube.com/watch?v=TeZZ9q8pqjQ>`__

The core Unicode support in the Python 2 series has the honour of being
documented in PEP 100.
It was created as `Misc/unicode.txt`_ in March 2000 (before the
PEP process even existed) to integrate Unicode 3.0 support into Python 2.0.
Once the PEP process was defined, it was deemed more appropriate to capture
these details as an informational PEP.

Guido, along with the wider Python and software development communities,
learned a lot about the best techniques for handling Unicode in the six years
between the introduction of Unicode support in Python 2.0 and inauguration
of the `python-3000 mailing list`_ in March 2006.

One of the most important guidelines for good Unicode handling is to ensure
that all encoding and decoding occurs at system boundaries, with all
internal text processing operating solely on Unicode data. The Python 2
Unicode model is essentially the POSIX text model with Unicode support
bolted on to the side, so it doesn't follow that guideline: it allows
implicit decoding at almost any point where an 8-bit string encounters a
Unicode string, along with implicit encoding at almost any location where
an 8-bit string is needed but a Unicode string is provided.

One reason this approach is problematic is that it means the traceback for
an unexpected :exc:`UnicodeDecodeError` or :exc:`UnicodeEncodeError` in a
large Python 2.x code base almost *never* points you to the code that is
broken. Instead, you have to trace the origins of the *data* in the failing
operation, and try to figure out where the unexpected 8-bit or Unicode code
string was introduced. By contrast, Python 3 is designed to fail fast in
most situations: when a :exc:`UnicodeError` of any kind occurs, it is more
likely that the problem actually does lie somewhere close to the operation
that failed. In those cases where Python 3 doesn't fail fast, it's because
it is designed to "round trip" - so long as the output encoding matches
the input encoding (even if it turns out the data isn't properly encoded
according to that encoding), Python 3 will aim to faithfully reproduce the
input byte sequence as the output byte sequence.

The implicit nature of the conversions in Python 2 also means that encoding
operations may raise decoding errors and vice-versa, depending on the input
types and the codecs involved.

A more pernicious problem arises when Python 2 *doesn't* throw an exception
at all - this problem occurs when two 8-bit strings with data in different
text encodings are concatenated or otherwise combined. The result is invalid
data, but Python will happily pass it on to other applications in its
corrupted form. Python 3 isn't completely immune to this problem, but it
should arise in substantially fewer cases.

The general guiding philosophy of the text model in Python 3 is essentially:

* try to do the right thing by default
* if we can't figure out the right thing to do, throw an exception
* as far as is practical, always require users to opt in to behaviours
  that pose a significant risk of silently corrupting data in non-ASCII
  compatible encodings

Ned Batchelder's wonderful `Pragmatic Unicode`_ talk/essay could just as
well be titled "This is why Python 3 exists". There are a large number of
Unicode handling bugs in the Python 2 standard library that have not been,
and will not be, fixed, as fixing them within the constraints of the Python
2 text model is considered too hard to be worth the effort (to put that
effort into context: if you judge the core development team by our *actions*
it is clear that we consider that creating and promoting Python 3 was an
*easier* and *more pleasant* alternative to attempting to fix those issues
while abiding by Python 2's backwards compatibility requirements).

The revised text model in Python 3 also means that the *primary* string
type is now fully Unicode capable. This brings Python closer to the model
used in the JVM, Android, .NET CLR, and Unicode capable Windows APIs. One
key consequence of this is that the interpreter core in Python 3 is far
more tolerant of paths that contain Unicode characters on Windows (so,
for example, having a non-ASCII character in your username should no
longer cause any problems with running Python scripts from your home
directory on Windows). The ``surrogateescape`` error handler added in
:pep:`383` is designed to bridge the gap between the new text model in
Python 3 and the possibility of receiving data through bytes oriented APIs
on POSIX systems where the declared system encoding doesn't match the
encoding of the data itself. That error handler is also useful in other
cases where applications need to tolerate mismatches between declared
encodings and actual data - while it does share some of the problems of the
Python 2 Unicode model, it at least has the virtue of only causing problems
in the case of errors either in the input data or the declared encoding,
where Python 2 could get into trouble in the presence of multiple data
sources with *different* encodings, even if all the input was correctly
encoded in its declared encoding.

Python 3 also embeds Unicode support more deeply into the language itself.
With the primary string type handling the full Unicode range, it became
practical to make UTF-8 the default source encoding (instead of ASCII) and
adjust many parts of the language that were previously restricted to ASCII
text (such as identifiers) to now permit a much wider range of Unicode
characters. This permits developers with a native language other than English
to use names in their own language rather than being forced to use names
that fit within the ASCII character set. Some areas of the interpreter that
were previously fragile in the face of Unicode text (such as displaying
exception tracebacks) are also far more robust in Python 3.

Removing the implicit type conversions entirely also made it more practical
to implement the new internal Unicode data model for Python 3.3, where
the internal representation of Unicode strings is automatically adjusted
based on the highest value code point that needs to be stored (see
`PEP 393`_ for details).

.. _Misc/unicode.txt: http://svn.python.org/view/python/trunk/Misc/unicode.txt?view=log&pathrev=25264
.. _python-3000 mailing list: http://mail.python.org/pipermail/python-3000/
.. _PEP 393: http://www.python.org/dev/peps/pep-0393/
.. _Pragmatic Unicode: http://nedbatchelder.com/text/unipain.html


What actually changed in the text model between Python 2 and Python 3?
----------------------------------------------------------------------

The Python 2 core text model looks like this:

* ``str``: 8-bit type containing binary data, or encoded text data in an
  unknown (hopefully ASCII compatible) encoding, represented as length 1
  8-bit strings
* ``unicode``: 16-bit or 32-bit type (depending on build options) containing
  Unicode code points, represented as length 1 Unicode strings

That first type is essentially the way POSIX systems model text data, so it
is incredibly convenient for interfacing with POSIX environments, since it
lets you just copy bits around without worrying about their encoding. It is
also useful for dealing with the ASCII compatible segments that are part
of many binary protocols.

The conceptual problem with this model is that it is an appropriate model for
*boundary* code - the kind of code that handles the transformation between
wire protocols and file formats (which are always a series of bytes), and the
more structured data types actually manipulated by applications (which may
include opaque binary blobs, but are more typically things like text, numbers
and containers).

Actual *applications* shouldn't be manipulating values that "might be
text, might be arbitrary binary data". In particular, manipulating text
values as binary data in multiple different text encodings can easily cause
a problem the Japanese named "mojibake": binary data that includes text in
multiple encodings, but with no clear structure that defines which parts are
in which encoding.

Unfortunately, Python 2 uses a type with exactly those semantics as its core
string type, permits silent promotion from the "might be binary data" type
to the "is definitely text" type and provides little support for accounting
for encoding differences.

So Python 3 changes the core text model to be one that is more appropriate
for *application* code rather than boundary code:

* ``str``: a sequence of Unicode code points, represented as length 1
  strings (always contains text data)
* ``bytes``: a sequence of integers between 0 and 255 inclusive (always
  contains arbitrary binary data). While it still has many operations that
  are designed to make it convenient to work on ASCII compatible segments in
  binary data formats, it *is not* implicitly interoperable with the ``str``
  type.

The hybrid "might be encoded text, might be arbitrary binary data, can
interoperate with both other instances of str and also with instances of
unicode" type was *deliberately* removed from the core text model because
using the same type for multiple distinct purposes makes it incredibly
difficult to reason about correctly. The core model in Python 3 opts to
handle the "arbitrary binary data" case and the "ASCII compatible segments
in binary data formats" case, leaving the direct manipulation of encoded
text to a (currently still hypothetical) third party type (due to the many
issues that approach poses when dealing with multibyte and variable width
text encodings).

The purpose of boundary code is then to hammer whatever comes in over the
wire or is available on disk into a format suitable for passing on to
application code.

Unfortunately, there have turned out to be some key challenges in making
this model pervasive in Python 3:

* the same design changes that improve Python 3's Windows integration by
  changing several OS interfaces to operate on text rather than binary data
  also make it more sensitive to locale misconfiguration issues on
  POSIX operating systems other than Mac OS X. In Python 2, text is always
  sent and received from POSIX operating system interfaces as *binary* data,
  and the associated decoding and encoding operations are fully under the
  control of the application. In Python 3, the interpreter aims to handle
  these operations automatically, but in releases up to and including
  Python 3.6 it needs to rely on the default settings in the OS provided
  locale module to handle the conversion, making it potentially sensitive to
  configuration issues that many Python 2 applications could ignore. Most
  notably, if the OS erroneously claims that "ascii" is a suitable encoding
  to use for operating system interfaces (as happens by default in a number
  of cases, due to the formal definition of the ANSI C locale predating the
  invention of UTF-8 by a few years), the Python 3 interpreter will believe
  it, and will complain if asked to handle non-ASCII data. :pep:`538` and
  :pep:`540` offer some possible improvements in this area (by assuming UTF-8
  as the preferred text encoding when running in the default ``C`` locale), but
  it isn't a trivial fix due to the phase of the interpreter startup sequence
  where the problem occurs. (Thanks go to Armin Ronacher for clearly
  articulating many of these details - see his write-up in the
  `click <http://click.pocoo.org/python3/>`__ documentation)
* when migrating libraries and frameworks from Python 2 to Python 3 that
  handle boundary API problems, the lack of the hybrid "might be text, might
  be arbitrary bytes" type can be keenly felt, as the implicitly
  interoperable type was essential to being able to cleanly share code
  between the two modes of operation. This usually isn't a major problem
  for *new* Python 3 code - such code is typically designed to operate in
  the binary domain (perhaps relying on the methods for working with ASCII
  compatible segments), the text domain, or to handle a transition between
  them. However, code being ported from Python 2 may need to continue to
  implement hybrid APIs in order to accommodate users that make different
  decisions regarding whether to operate in the binary domain or the text
  domain in Python 3 - because Python 2 blurred the distinction, different
  users will make different choices, and third party libraries and
  frameworks may need to account for that rather than forcing a particular
  answer for all users.
* in the initial Python 3 design, interpolation of variables into a format
  string was treated solely as a text domain operation. While this proved to be
  a reasonable design decision for the flexible Python-specific ``str.format``
  operation, :pep:`461` restored printf-style interpolation for ASCII
  compatible segments in binary data in Python 3.5. Prior to that change, the
  lack of this feature could sometimes be an irritation when working extensively
  in Python 3 with wire protocols and file formats that include ASCII compatible
  segments.
* while the API design of the ``str`` type in Python 3 was based directly on
  the ``unicode`` type in Python 2, the ``bytes`` type doesn't have such a
  clean heritage. Instead, it evolved over the course of the initial Python 3
  pre-release design period, starting from a model where the *only* type for
  binary data handling was the type now called ``bytearray``. That type was
  modelled directly on the ``array.array('B')`` type, and hence produced
  integers when iterating over it or indexing into it. During the pre-release
  design period, the lack of an immutable binary data type was identified as
  a problem, and the (then mutable) ``bytes`` type was renamed to
  ``bytearray`` and a new immutable ``bytes`` type added. The now familiar
  "bytes literal" syntax was introduced (prepending a "b" prefix to the
  string literal syntax) and the representations of the two types were also
  adjusted to be based on the new bytes literal syntax. With the benefit of
  hindsight, it has become clear another change should have been made at the
  same time: with so many affordances switched back to matching those of the
  Python 2 ``str`` type (including the use of the new bytes literal syntax to
  refer to that type in Python 2.6 and 2.7), ``bytes`` and ``bytearray``
  should have been been switched away from behaving like a tuple of integers
  and list of integers (respectively) and instead modified to be containers
  of length 1 ``bytes`` objects, just as the ``str`` type is a container of length 1
  ``str`` objects. Unfortunately, that change was not made at the time, and
  now backwards compatibility constraints within the Python 3 series itself
  makes it highly unlikely the behaviour will be changed in the future
  either. :pep:`467` covers a number of other still visible remnants of
  this convoluted design history that are more amenable to being addressed
  within the constraints of Python's normal Python deprecation processes.

These changes are a key source of friction when it comes to Python 3 between
the Python core developers and other experts that had fully mastered the
Python 2 text model, especially those that focus on targeting POSIX
platforms rather than Windows or the JVM, as well as those that focus on
writing boundary code, such as networking libraries, web frameworks and
file format parsers and generators. These developers bore a lot of the
burden of adjusting to these changes on behalf of their users, often while
gaining few or none of the benefits.

That said, while these issues certainly aren't ideal, they also won't impact
many users that are relying on libraries and frameworks to deal with boundary
issues, and can afford to ignore possible misbehaviour in misconfigured POSIX
environments. As Python 3 has matured as a platform, most of those
areas where it has regressed in suitability relative to Python 2 have been
addressed. In particular, the ongoing migrations of Linux distribution
utilities from Python 2 to Python 3 have seen many of the platform
integration issues on POSIX systems dealt with in a cleaner fashion. The
tuple-of-ints and list-of-ints behaviour of ``bytes`` and ``bytearray`` is
unlikely to change, but proposals like :pep:`467` may bring better tools
for dealing with them.


Why not just assume UTF-8 and avoid having to decode at system boundaries?
--------------------------------------------------------------------------

The design decision to go with a fixed width Unicode representation both
externally and internally has a long history in Python, going all the way
back to the addition of Python's original Unicode support in Python 2.0.
Using a fixed width type at that point meant that many of the algorithms
could be shared between the original 8-bit ``str`` type and the new
16-or-32-bit ``unicode`` type. (Note that adoption of this particular
approach predates my own involvement in CPython core development - as with
many other aspects of CPython's text handling support, it's something I've
learned about while helping with the transition to pervasive Unicode support
in the standard library and elsewhere for Python 3).

That design meant that, historically, CPython builds had to choose what size
to use for the internal representation of Unicode text. We always chose to
use "narrow" builds for the Windows binary installers published on
python.org, as the UTF-16 internal representation was the best fit for the
Windows text handling APIs.

Linux distributions, by contrast, almost all chose the memory hungry "wide"
builds that allocated 32 bits per Unicode code point in Python 2 ``unicode``
objects and Python 3 ``str`` objects (up to & including Python 3.2), even for
pure ASCII text. There's a reason they went for that option, though: it was
better at handling Unicode code points outside the basic multilingual plane.
In narrow builds the UTF-16 code points were exposed directly in both the C
API and the Python API of the ``unicode`` type, and hence were prone to bugs
related to incorrect handling of code points greater than 65,535 in code that
assumed a one-to-one correspondence between Python code points and Unicode
code points. This wasn't generally a big deal when code points in common use
all tended to fit in the BMP, but started to become more problematic as
things like mathematical and musical notation, ancient languages, emoticons
and additional CJK ideographs were added. Given the choice between greater
memory efficiency and correctness, the Linux distributions chose correctness,
imposing a non-trivial memory usage penalty on Unicode heavy applications
that couldn't rely entirely on ``str`` objects in Python 2 or ``bytes`` and
``bytearray`` objects in Python 3. Those larger strings also came at a cost
in speed, since they not only meant having more data to move around relative
to narrow builds (or applications that only allowed 8-bit text), but the
larger memory footprint also made CPU caches less effective.

When it came to the design of the C level text representation for Python
3, the existing Python 2 Unicode design wasn't up for reconsideration - the
Python 2 ``unicode`` type was mapped directly to the Python 3 ``str`` type.
This is most obvious in the Python 3 C API, which still uses the same
``PyUnicode_*`` prefix for text manipulation APIs, as that was the easiest
way to preserve compatibility with C extensions that were originally written
against Python 2.

However, removing the intertwining of the 8-bit str type and the unicode
type that existed in Python 2 paved the way for eliminating the narrow
vs wide build distinction in Python 3.3, and eliminating a significant
portion of the memory cost associated with getting correct Unicode handling
in earlier versions of Python. As a result of :pep:`393`, strings that
consist solely of latin-1 or UCS2 code points in Python 3.3+ are able to use
8 or 16 bits per code point (as appropriate), while still being able to use
string manipulation algorithms that rely on the assumption of consistent code
point sizes within a given string. As with the original Python 3
implementation, there were also a large number of constraints imposed on
this redesign of the internal representation based on the public C API, and
that is reflected in some of the more complicated aspects of the PEP.

While it's theoretically possible to write string manipulation algorithms
that work correctly with variable width encodings (potentially saving even
more memory), it isn't *easy* to do so, and for cross-platform runtimes that
interoperate closely with the underlying operating system the way CPython
does, there isn't an obvious universally correct choice even today, let alone
back in 2006 when Guido first started the Python 3 project. UTF-8 comes
closest (hence the wording of this question), but it still poses risks of
silent data corruption on Linux if you don't explicitly transcode data at
system boundaries (particularly if the actual encoding of metadata provided
by the system is ASCII incompatible, as can happen in East Asian countries
using encodings like Shift-JIS and GB-18030) and still requires transcoding
between UTF-16-LE and UTF-8 on Windows (the bytes-oriented APIs on Windows are
generally restricted to the ``mbcs`` encoding, making them effectively
useless for proper Unicode handling - it's necessary to switch to the
Windows specific UTF-16 based APIs to make things work properly).

The Python 3 text model also trades additional memory usage for encoding
and decoding speed in some cases, including caching the UTF-8
representation of a string when appropriate. In addition to UTF-8, other key
codecs like ASCII, latin-1, UTF-16 and UTF-32 are closely
integrated with the core text implementation in order to make them as
efficient as is practical.

The current Python 3 text model certainly has its challenges, especially
around Linux compatibility (see :pep:`383` for an example of the complexity
associated with that problem), but those are considered the lesser evil when
compared to the alternative of breaking C extension compatibility and having
to rewrite all the string manipulation algorithms to handle a variable width
internal encoding, while still facing significant integration challenges on
both Windows and Linux. Instead of anyone pursuing such a drastic change, I
expect the remaining Linux integration issues for the existing model to be
resolved as we help Linux distributions like Ubuntu and Fedora migrate their
system services to Python 3 (in the specific case of Fedora, that migration
encompasses both the operating system installer *and* the package manager).

Still, for new runtimes invented today, particularly those aimed primarily
at new server applications running on Linux that can afford to ignore the
integration challenges that arise on Windows and older Linux systems using
encodings other than UTF-8, using UTF-8 for their internal string
representation makes a lot of sense. It's just best to avoid exposing the raw
binary representation of text data for direct manipulation in user code:
experience has shown that a Unicode code point based abstraction is much
easier to work with, even if it means opting out of providing O(1) indexing
for arbitrary code points in a string to avoid allocating additional memory
per code point based on the largest code point in the string. For new
languages that are specifically designed to accommodate a variable width
internal encoding for text, a file-like opaque token based seek/tell style
API is likely to be more appropriate for random access to strings than a
Python style integer based indexing API. The kind of internal flexibility
offered by the latter approach can be seen in Python's own ``io.StringIO``
implementation - in Python 3.4+, that aims to delay creation of a full string
object for as long as possible, an optimisation that could be implemented
transparently due to the file-like API that type exports.

.. note:: Python 3 does assume UTF-8 at system boundaries on Mac OS X, since
   that OS ensures that the assumption will almost always be correct. Starting
   with Python 3.6, CPython on Windows also assumes that binary data passed to
   operating system interfaces is in UTF-8 and transcodes it to UTF-16-LE before
   passing it to the relevant Windows APIs.

   For Python 3.7, :pep:`538` and :pep:`540` are likely to extend the UTF-8
   assumption to the default ``C`` locale more generally (so other system
   encodings will still be supported through the locale system, but the
   problematic ASCII default will be largely ignored).


OK, that explains Unicode, but what about all the other incompatible changes?
-----------------------------------------------------------------------------

The other backwards incompatible changes in Python 3 largely fell into the
following categories:

* dropping deprecated features that were frequent sources of bugs in
  Python 2, or had been replaced by superior alternatives and retained
  solely for backwards compatibility
* reducing the number of statements in the language
* replacing concrete list and dict objects with more memory efficient
  alternatives
* renaming modules to be more PEP 8 compliant and to automatically use C
  accelerators when available

The first of those were aimed at making the language easier to learn, and
easier to maintain. Keeping deprecated features around isn't free: in order
to maintain code that uses those features, everyone needs to remember them
and new developers need to be taught them. Python 2 had acquired a lot of
quirks over the years, and the 3.x series allowed such design mistakes to be
corrected.

While there were advantages to having ``print`` and ``exec`` as statements,
they introduced a sharp discontinuity when switching from the statement forms
to any other alternative approach (such as changing ``print`` to
``logging.debug`` or ``exec`` to ``execfile``), and also required the use of
awkward hacks to cope with the fact that they couldn't accept keyword
arguments. For Python 3, they were demoted to builtin functions in order
to remove that discontinuity and to exploit the benefits of keyword only
parameters.

The increased use of iterators and views was motivated by the fact that
many of Python's core APIs were designed *before* the introduction of
the iterator protocol.
That meant a lot unnecessary lists were being created when more memory
efficient alternatives were now possible.
We didn't get them all (you'll still find APIs that unnecessarily return
concrete lists and dictionaries in various parts of the standard library),
but the core APIs are all now significantly more memory efficient by default.

As with the removal of deprecated features, the various renaming operations
were designed to make the language smaller and easier to learn. Names that
don't follow standard conventions need to be remembered as special cases,
while those that follow a pattern can be derived just be remembering the
pattern. Using the API compatible C accelerators automatically also means
that end users no longer need to know about and explicitly request the
accelerated variant, and alternative implementations don't need to provide
the modules under two different names.

No backwards incompatible changes were made just for the sake of making them.
Each one was justified (at least at the time) on the basis of making the
language either easier to learn or easier to use.

With the benefit of hindsight, a number of these other changes would probably
have been better avoided (especially some of the renaming ones), but even those
cases at least seemed like a good idea at the time. At this point, internal
backwards compatibility requirements within the Python 3.x series mean it
isn't worth the hassle of changing them back, especially given the existence
of the `six`_ compatibility project and other third party modules that
support both Python 2 and Python 3 (for example, the ``requests`` package
is an excellent alternative to using the low level ``urllib`` interfaces
directly, even though ``six`` does provide appropriate cross-version
compatible access through the ``six.moves.urllib`` namespace).


What other notable changes in Python 3 depend on the text model change?
-----------------------------------------------------------------------

One of the consequences of the intertwined implementations of the ``str``
and ``unicode`` types in Python 2 is that it made it difficult to update
them to correctly interoperate with anything *else*. The dual type text
model also made it quite difficult to add Unicode support to various APIs
that previously didn't support it.

This isn't an exhaustive list, but here are several of the enhancements
in Python 3 that would likely be prohibitively difficult to backport to
Python 2 (even when they're technically backwards compatible):

* :pep:`393` (more efficient text storage in memory)
* Unicode identifier support
* full Unicode module name support
* improvements in Unicode path handling on Windows
* multiple other improvements in Unicode handling when interfacing with
  Windows APIs
* more robust and user friendly handling of Unicode characters in object
  representations and when displaying exceptions
* increased consistency in Unicode handling in files and at the interactive
  prompt (although the C locale on POSIX systems still triggers undesirable
  behaviour in Python 3)
* greater functional separation between text encodings and other codecs,
  including tailored exceptions nudging users towards the more generic
  APIs when needed (this change in Python 3.4 also eliminates certain
  classes of remote DOS attack targeted at the compression codecs in the
  codec machinery when using the convenience methods on the core types
  rather than the unrestricted interfaces in the codecs module)
* using the new IO model (with automatic encoding and decoding support) by
  default


What are (or were) some of the key dates in the Python 3 transition?
--------------------------------------------------------------------

.. note::

   This list is rather incomplete and I'm unlikely to find the time to
   complete it - if anyone is curious enough to put together a more
   comprehensive timeline, feel free to use this answer as a starting point,
   or else just send a PR to add more entries to this list.

   At least the following events should be included in a more complete list:

   * NumpPy 1.5.0 and SciPy 0.9.0 (these added Python 3 support)
   * matplotlib Python 3 support
   * IPython Python 3 support
   * Cython Python 3 support
   * SWIG Python 3 support
   * links for the Ubuntu, Fedora and openSUSE "Python 3 as default" migration
     plans
   * SQL Alchemy Python 3 support
   * pytz Python 3 support
   * PyOpenSSL support
   * mod_wsgi Python 3 support (first 3.x WSGI implementation)
   * Tornado Python 3 support (first 3.x async web server)
   * Twisted Python 3 support (most comprehensive network protocol support)
   * Pyramid Python 3 support (first major 3.x compatible web framework)
   * Django 1.5 and 1.6 (experimental and stable Python 3 support)
   * Werkzeug and Flask Python 3 support
   * requests Python 3 support
   * pyside Python 3 support (first Python 3.x Qt bindings)
   * pygtk and/or pygobject Python support
   * wxPython phoenix project
   * VTK Python 3 support in August 2015 (blocked Mayavi, which blocked Canopy)
   * cx-Freeze Python 3 support
   * setuptools and pip Python 3 support
   * Pillow (PIL fork) Python 3 support
   * greenlet Python 3 support
   * pylint Python 3 support
   * nose2 Python 3 support
   * pytest Python 3 support
   * Editor/IDE support for Python 3 in: PyDev, Spyder,
     Python Tools for Visual Studio, PyCharm, WingIDE, Komodo (others?)
   * Embedded Python 3 support in: Blender, Kate, vim, gdb, gcc, LibreOffice
     (others?)
   * version availability in services like Google DataLab and Azure Notebooks
   * Python 3 availability in Heroku
   * availability in the major Chinese public cloud platforms (Alibaba/Aliyun,
     Tencent Qcloud, Huawei Enterprise Cloud, etc)
   * the day any bar on https://python3wos.appspot.com/ or
     wedge on http://py3readiness.org/ turned green was potentially
     a significant step for some subsection of the community :)

.. _timeline-2006:

2006
^^^^

**March 2006**: Guido van Rossum (the original creator of Python and
hence Python's Benevolent Dictator for Life), with financial support
from Google, took the previously hypothetical "Python 3000" project
and turned it into an active development project, aiming to create
an updated Python language definition and reference interpreter
implementation that addressed some fundamental limitations in the
ability of the Python 2 reference interpreter to correctly handle
non-ASCII text. (The project actually started earlier than this - March
2006 was when the python-3000 list was created to separate out the longer
term Python 3 discussions from the active preparation for the Python 2.5
final release)

**April 2006**: Guido published :pep:`3000`, laying the ground rules for
Python 3 development, and detailing the proposed migration strategy
for Python 2 projects (the recommended porting approach has changed
substantially since then, see :ref:`other-changes` for more details).
:pep:`3100` describes several of the overall goals of the project, and
lists many smaller changes that weren't covered by their own PEPs.
:pep:`3099` covers a number of proposed changes that were explicitly
declared out of scope of the Python 3000 project.

At this point in time, Python 2 and Python 3 started being developed in
parallel by the core development team for the reference interpreter.

.. _timeline-2007:

2007
^^^^

**August 2007**: The first alpha release of Python 3.0 was published.

.. _timeline-2008:

2008
^^^^

**February 2008**: The first alpha release of Python 2.6 was published
alongside the third alpha of Python 3.0. The release schedules for both
Python 2.6 and 3.0 are covered in :pep:`361`.

**October 2008**: Python 2.6 was published, including the backwards
compatible features defined for Python 3.0, along with a number of
``__future__`` imports and the ``-3`` switch to help make it practical
to add Python 3 support to existing Python 2 software (or to migrate
entirely from Python 2 to Python 3). While Python 2.6 received its final
upstream security update in October 2013, maintenance & support remains
available through some commercial redistributors.

**December 2008**: In a fit of misguided optimism, Python 3.0 was published
with an unusably slow pure Python IO implementation - it worked tolerably
well for small data sets, but was entirely impractical for handling
realistic workloads on the CPython reference interpreter. (Python 3.0
received a single maintenance release, but was otherwise entirely
superceded by the release of Python 3.1)

ActiveState became the first company I am aware of to start offering
commercial Python 3 support by shipping ActivePython 3.0 almost immediately
after the upstream release was published. They have subsequently continued this
trend of closely following upstream Python 3 releases.

.. _timeline-2009:

2009
^^^^

**March 2009**: The first alpha release of Python 3.1, with an updated
C accelerated IO stack, was published. :pep:`375` covers the details of the
Python 3.1 release cycle.

**June 2009**: Python 3.1 final was published, providing the first version
of the Python 3 runtime that was genuinely usable for realistic workloads.
Python 3.1 received its final security update in April 2012, and even commercial
support for this version is no longer available.

**October 2009**: :pep:`3003` was published, declaring a moraratorium on
language level changes in Python 2.7 and Python 3.2. This was done to
deliberately slow down the pace of core development for a couple of years,
with additional effort focused on standard library improvements (as well
as some improvements to the builtin types).

**December 2009**: The first alpha of Python 2.7 was published. :pep:`373`
covers the details of the Python 2.7 release cycle.

.. _timeline-2010:

2010
^^^^

**July 2010**: Python 2.7 final was published, providing many of the
backwards compatible features added in the Python 3.1 and 3.2 releases.
Python 2.7 is currently still fully supported by the core development team
and will continue receiving maintenance & security updates until at least
January 2020.

Once the Python 2.7 maintenance branch was created, the py3k development
branch was retired: for the first time, the default branch in the main
CPython repo was the upcoming version of Python 3.

**August 2010**: The first alpha of Python 3.2 was published. :pep:`392`
covers the details of the Python 3.2 release cycle. Python 3.2 restored
preliminary support for the binary and text transform codecs that had
been removed in Python 3.0.

**October 2010**: :pep:`3333` was published to define WSGI 1.1, a Python 3
compatible version of the Python Web Server Gateway Interface.

.. _timeline-2011:

2011
^^^^

**February 2011**: Python 3.2 final was published, providing the first
version of Python 3 with support for the Web Server Gateway Interface.
Python 3.2 received its final security update in February 2016, and even
commercial support for this version is no longer available.

**March 2011**: After Arch Linux updated their Python symlink to
refer to Python 3 (breaking many scripts that expected it to refer to
Python 2), :pep:`394` was published to provide guidance to Linux
distributions on more gracefully handling the transition from Python 2 to
Python 3.

Also in March, CPython migrated from Subversion to Mercurial
(see :pep:`385`), with the first message from Mercurial to the
python-checkins list being `this commit from Senthil Kumaran
<https://mail.python.org/pipermail/python-checkins/2011-March/103828.html>`__.
This ended more than two years of managing parallel updates of four active
branches using ``svnmerge`` rather than a modern DVCS.

**November 2011**: :pep:`404` (the Python 2.8 Un-release Schedule) was
published to make it crystal clear that the core development team had no plans
to make a third parallel release in the Python 2.x series.

.. _timeline-2012:

2012
^^^^

**March 2012**: The first alpha of Python 3.3 was published. :pep:`398`
covers the details of the Python 3.3 release cycle. Notably, Python
3.3 restored support for Python 2 style Unicode literals after Armin
Ronacher and other web framework developers pointed out that this was one
change that the web frameworks couldn't handle on behalf of their users.
:pep:`414` covers the detailed rationale for that change.

**April 2012**: Canonical published Ubuntu 12.04 LTS, including commercial
support for both Python 2.7 and Python 3.2.

**September 2012**: Six and half years after the inauguration of the Python
3000 project, Python 3.3 final was published as the first Python
3 release without a corresponding Python 2 feature release. This release
introduced the :pep:`380` ``yield from`` syntax that was used heavily in the
``asyncio`` coroutine framework provisionally introduced to the standard library
in Python 3.4, and subsequently declared stable in Python 3.6.

**October 2012**: :pep:`430` was published, and the `online Python
documentation <http://docs.python.org>`__ updated to present the Python 3
documentation by default. In order to preserve existing links, deep links
continue to be interpreted as referring to the Python 2.7 documentation.

.. _timeline-2013:

2013
^^^^

**March 2013**: :pep:`434` redefined IDLE as an application shipped with
Python rather than part of the standard library, allowing the addition of
new features in maintenance releases. Significantly, this allowed the
Python 2.7 IDLE to be brought more into line with the features of the Python
3.x version.

Continuum Analytics started offering commercial support for cross-platform
Python 3.3+ environments through their "Anaconda" Python distributions.

**August 2013**: The first alpha of Python 3.4 was published. :pep:`429`
covers the details of the Python 3.4 release cycle. Amongst other changes,
Python 3.4 restored full support for the binary and text transform codecs
that were reinstated in Python 3.2, while maintaining the "text encodings
only" restriction for the convenience methods on the builtin types.

**September 2013**: Red Hat published "Red Hat Software Collections 1.0",
providing commercial support for both Python 2.7 and Python 3.3 on Red
Hat Enterprise Linux systems, with later editions adding support for
additional 3.x releases.

**December 2013**: The initial development of MicroPython, a variant of Python
3 specifically for microcontrollers, was successfully crowdfunded on
Kickstarter.

.. _timeline-2014:

2014
^^^^

**March 2014**: Python 3.4 final was published as the second Python 3
release without a corresponding Python 2 release. It included several
features designed to provide a better starting experience for newcomers
to Python, such as bundling the "pip" installer by default, and including
a rich asynchronous IO library.

**April 2014**: Ubuntu 14.04 LTS, initial target release for the "Only
Python 3 on the install media" Ubuntu migration plan. (They didn't quite
`make it <https://wiki.ubuntu.com/Python/3>`__ - a few test packages short on
Ubuntu Touch, further away on the server and desktop images)

Red Hat also announced the creation of `softwarecollections.org
<http://developerblog.redhat.com/2014/04/08/announcing-softwarecollections-org/>`__
as the upstream project powering the Red Hat Software Collections product.
The whole idea of both the project and the product is to make it easy to run
applications using newer (or older!) language, database and web server
runtimes, without interfering with the versions of those runtimes integrated
directly into the operating system.

.. note::

   With the original "5 years for migration to Python 3" target date
   approaching, April 2014 is also when Guido van Rossum amended the
   :pep:`Python 2.7 release PEP <373>` to move the expected end-of-life date
   for Python 2.7 out to 2020.

**May 2014**: Python 2.7.7 was published, the first Python 2.7 maintenance
release to incorporate additional security enhancement features as described in
:pep:`466`. Also the first release where Microsoft contributed developer
time to the creation of the Windows installers.

**June 2014**: The first stable release of PyPy3, providing a version of
the PyPy runtime that is compatible with Python 3.2.5 (together with
:pep:`414`'s restoration of the ``u''`` string literal prefix that first
appeared in Python 3.3 for CPython).

Red Hat published Red Hat Enterprise Linux 7, with Python 2.7 as the system
Python. This release ensures that Python 2.7 will remain a commercially
supported platform until *at least* 2024 (based on Red Hat's 10 year support
lifecycle).

.. note::

   June 2014 also marked 5 years after the first production capable
   Python 3.x release (Python 3.1), and the original target date for
   completion of the Python 3 migration.

**July 2014**: CentOS 7 was released, providing a community distro based on
Red Hat Enterprise Linux 7, and marking the beginning of the end of the Python
2.7 rollout (the CentOS system Python is a key dependency for many Python
users).

boto v2.32.0 released with Python 3 support for most modules.

nltk 3.0b1 released with Python 3 support and the NLTK book switched over to
covering Python 3 by default.

.. _timeline-2015:

2015
^^^^

**February 2015**: The first alpha of Python 3.5 was published. :pep:`478`
covers the details of the Python 3.5 release cycle. Amongst other changes,
:pep:`461` restored support for printf-style interpolation of binary data,
addressing a significant usability regression in Python 3 relative to Python 2.

**October 2014**: SUSE Linux Enterprise Server 12 was released, containing
supported Python 3.4 RPMs, adding SUSE to the list of commercial Python 3
redistributors.

**March 2015**: Microsoft Azure App Service launched with both Python 2.7 and
Python 3.4 support, adding Microsoft to the list of commercial Python
redistributors for the first time.

**August 2015**: At the Fedora community's annual Flock conference, Denise
Dumas (Red Hat's VP of Platform Engineering), explicitly states that it is an
engineering goal to include only Python 3 in the base operating system for the
next major version of Red Hat Enterprise Linux (previously this had been implied
by Red Hat's work on migrating Fedora and its infrastructure to Python 3, but
not explicitly stated in a public venue)

**September 2015**: Python 3.5 final was released, bringing native syntactic
support for asynchronous coroutines and a matrix multiplication operator, as
well as the typing module for static type hints. Applications, libraries and
frameworks wishing to take advantage of the new syntactic features need to
reconsider whether or not to continue supporting Python 2.7.

Twisted 15.4 was released, the first version to include a Python 3 compatible
version of the "Twisted Trial" test runner. This allowed the Twisted project
to start running its test suite under Python 3, leading to steadily increasing
Python 3 compatibility in subsequent Twisted releases.

**October 2015**: Fedora 23 ships with only Python 3 in the LiveCD and all
default images other than the Server edition.

MicroPython support for the BBC micro:bit project is
publicly announced, ensuring first class Python 3 support in a significant
educational initiative.

PyInstaller 3.0 was released, supporting Python 2.7, and 3.3+.

.. _timeline-2016:

2016
^^^^

**March 2016**: gevent 1.1 was released, supporting Python 2.6, 2.7, and 3.3+.

**May 2016**: Several key projects in the Scientific Python community publish
the `Python 3 Statement <http://www.python3statement.org/>`_, explicitly
declaring their intent to end Python 2 support in line with the reference
interpreter's anticipated 2020 date for the end of free community support.

**August 2016**: Google App Engine added official Python 3.4(!) support to their
Flexible Environments (Python 3.5 support followed not long after, but the
original announcement was for Python 3.4).

As part of rolling out Python 3.5 support, Microsoft Azure published
instructions on how to select a particular Python version using
`App Service Site Extensions <https://blogs.msdn.microsoft.com/pythonengineering/2016/08/04/upgrading-python-on-azure-app-service/>`__.

Initial release of Enthought Deployment Manager, with support for Python 2.7
and 3.5.

Mozilla provided the PyPy project with a
`development grant <https://morepypy.blogspot.com.au/2016/08/pypy-gets-funding-from-mozilla-for.html>`__
to bring their PyPy3 variant up to full compatibility with Python 3.5.

**December 2016**: Python 3.6 final was released, bringing further syntactic
enhancements for asynchronous coroutines and static type hints, as well as a
new compiler assisted string formatting syntax that manages to be both more
readable (due to the use of inline interpolation expressions) and faster (due
to the compiler assisted format parsing) than previous string formatting
options. Through :pep:`528` and :pep:`529`, this release also featured
significant improvements to the Windows compatibility of bytes-centric
POSIX applications, and the Windows-specific `py` launcher started using Python
3 by default when both Python 2.x and 3.x are available on the system.

.. _timeline-2017:

2017
^^^^

**March 2017**: The first beta release of PyPy3 largely compatible with
Python 3.5 was
`published <https://morepypy.blogspot.com.au/2017/03/pypy27-and-pypy35-v57-two-in-one-release.html>`__
(including support for the Python 3.6 f-string syntax).

Enthought Canopy 2.0.0 available, supporting Python 2.7 and 3.5 (official
binary release date TBD - as of April 2017, the download page still offers
Canopy 1.7.4)

**April 2017**: AWS Lambda added official Python 3.6 support, making Python 3
available by default through the 3 largest public cloud providers (Amazon,
Microsoft, Google).

IPython 6.0 was released, the first feature release to require
Python 3. The IPython 5.x series remains in maintenance mode as the last
version supporting Python 2.7 (and Python 3 based variants of IPython retain
full support for running and interacting with Python 2 language kernels using
Project Jupyter's language independent notebook protocol).

**December 2017**: Django `released Django 2.0
<https://www.djangoproject.com/weblog/2017/dec/02/django-20-released/>`__,
the first version of Django to `drop support for Python 2.7
<https://docs.djangoproject.com/en/2.2/releases/2.0/>`__.

.. _timeline-2018:

2018
^^^^

**March 2018**: Guido van Rossum `clarified
<https://mail.python.org/archives/list/python-dev@python.org/message/JIVZVIGYTW3EZZDDDRN3O3XQFX7FIVE7/>`__
that "The way I see the situation for 2.7 is that EOL is January 1st,
2020, and there will be no updates, not even source-only security
patches, after that date. Support (from the core devs, the PSF, and
python.org) stops completely on that date. If you want support for 2.7
beyond that day you will have to pay a commercial vendor."

.. _timeline-2019:

2019
^^^^

**August 2019**: The entirety of http://py3readiness.org/ `turned
green
<https://twitter.com/py3readiness/status/1158663735436894208>`__,
indicating Python 3 support for the 360 most downloaded packages on
PyPI.


.. _timeline-future:

Future
^^^^^^

.. note:: At time of writing, the events below are in the future, and hence
   speculative as to their exact nature and timing. However, they reflect
   currently available information based on the stated intentions of developers
   and distributors.


**April 2018**: Revised anticipated date for Ubuntu and Fedora to have finished
migrating default components of their respective server editions to
Python 3 (some common Linux components, most notably the Samba protocol server,
proved challenging to migrate, so the stateful server variants of these
distributions ended up taking longer to migrate to Python 3 than other variants
that omitted those components from their default package set)

**January? 2020**: Anticipated date for Python 2.7 to switch to security
fix only mode, ending roughly thirteen years of parallel maintenance of
Python 2 and 3 by the core development team for the reference interpreter.

**April 2021**: Anticipated date for Ubuntu LTS 16.04 to go end of life, the
first potential end date for commercial Python 2 support from Canonical (if
Python 2.7 is successfully migrated to the community supported repositories for
the Ubuntu 18.04 LTS release)

**April 2024**: Anticipated date for Ubuntu LTS 18.04 to go end of life, the
second potential end date for commercial Python 2 support from Canonical (if it
proves necessary to keep Python 2.7 in the commercially supported repositories
as a dependency for the Ubuntu 18.04 LTS release)

**June 2024**: Anticipated date for Red Hat Enterprise Linux 7 to go end of
life, also anticipated to be the last commercially supported redistribution of
the Python 2 series.


When did Python 3 become the obvious choice for new projects?
-------------------------------------------------------------

I put the date for this as the release of Python 3.5, in September 2015. This
release brought with it two major syntactic enhancemens (one giving Python's
coroutine support its own dedicated syntax, distinct from generators, and
another providing a binary operator for matrix multiplication), and restored
a key feature that had been missing relative to Python 2 (printf-style binary
interpolation support). It also incorporated a couple of key reliability and
maintainability enhancements, in the form of automated handling of EINTR
signals, and the inclusion of a gradual typing framework in the standard
library.

Others may place the boundary at the release of Python 3.6, in December 2016,
as the new "f-string" syntax provides a form of compiler-assisted string
interpolation that is both faster and more readable than its predecessors::

    print("Hello %s!" % name)        # All versions
    print("Hello {0}!".format(name)) # Since Python 2.6 & 3.0
    print("Hello {}!".format(name))  # Since Python 2.7 & 3.2
    print(f"Hello {name}!")          # Since Python 3.6

Python 3.6 also provides further enhancements to the native coroutine syntax,
as well as full syntactic support for annotating variables with static type
hints.

Going in to this transition process, my personal estimate was that
it would take roughly 5 years to get from the first production ready release
of Python 3 to the point where its ecosystem would be sufficiently mature for
it to be recommended unreservedly for all *new* Python projects.

Since 3.0 turned out to be a false start due to its IO stack being unusably
slow, I start that counter from the release of 3.1: June 27, 2009.
With Python 3.5 being released a little over 6 years after 3.1 and 3.6 a little
more than a year after that, that means we clearly missed that original goal -
the text model changes in particular proved to be a larger barrier to migration
than expected, which slowed adoption by existing library and framework
developers.

However, despite those challenges, key parts of the ecosystem were able to
successfully add Python 3 support well before the 3.5 release. NumPy and the
rest of the scientific Python stack supported both versions by 2015, as did
several GUI frameworks (including PyGame).

The Pyramid, Django and Flask web frameworks supported both versions, as did
the mod_wsgi Python application server, and the py2exe, py2app and cx-Freeze
binary creators. The upgrade of Pillow from a repackaging project to a full
development fork also brought PIL support to Python 3.

nltk supported Python 3 as of nltk 3.0, and the NLTK bookswitched to be based
on Python 3 at the same time.

For AWS users, most ``boto`` modules became available on Python 3 as of
`http://boto.readthedocs.org/en/latest/releasenotes/v2.32.0.html <boto
v2.32.0>`__.

PyInstaller is a popular option for creating native system installers for Python
applications, and it has supported Python 3 since the 3.0 release in October
2015.

gevent is a popular alternative to writing natively asynchronous code, and it
became generally available for Python 3 with the 1.1 release in March 2016.

As of April 2017, porting the full Twisted networking framework to Python 3 is
still a work in progress, but many parts of it are already fully operational,
and for new projects, native asyncio-based alternatives are often going to be
available in Python 3 (especially for common protocols like HTTPS).

I think Python 3.5 is a superior language to 2.7 in almost every way (with
the error reporting improvements being the ones I missed most when my day job
involved working on a Python 2.6 application).

For educational purposes, there are a few concepts like functions, iterables
and Unicode that need to be introduced earlier than was needed in Python 2, and
there are still a few rough edges in adapting between the POSIX text model and
the Python 3 one, but these are more than compensated for through improved
default behaviours and more helpful error messages.

While students in enterprise environments may still need to learn Python 2 for
a few more years, there are some significant benefits in learning Python 3
*first*, as that means students will already know which concepts survived the
transition, and be more naturally inclined to write code that fits into the
common subset of Python 2 and Python 3. This approach will also encourage
new Python users that need to use Python 2 for professional reasons to take
advantage of the backports and other support modules on PyPI to bring their
Python 2.x usage as close to writing Python 3 code as is practical.

Support in enterprise Linux distributions is also a key point for uptake
of Python 3. Canonical have already shipped long term support for three
versions of Python 3 (Python 3.2 in Ubuntu 12.04 LTS, 3.4 in 14.04 LTS, and
3.5 in 14.04 LTS) and are continuing with `the process of eliminating`_
Python 2 from the installation images.

A Python 3 stack has existed in Fedora since Fedora 13 and has been
growing over time, with Python 2 successfully removed from the live install CDs
in `late 2015`_ (Fedora 23). Red Hat also now ship fully supported Python 3.x
runtimes as part of the `Red Hat Software Collections`_ product and the
OpenShift Enterprise self-hosted Platform-as-a-Service offering (with new 3.x
versions typically becoming commercially available within 6-12 months of the
upstream release, and then remaining supported for 3 years from that point).

At Fedora's annual Flock conference in August 2015, Denise Dumas (VP of Platform
Engineering) also indicated that Red Hat aimed to have the next major version of
Red Hat Enterprise Linux ship only Python 3 in the base operating system, with
Python 2 available solely through the Software Collections model (inverting the
current situation, where Python 2 is available in both Software Collections and
the base operating system, while Python 3 is only commercially available through
Software Collections and the Software Collections based OpenShift environments).

The Arch Linux team have gone even further, making Python 3 the
`default Python`_ on Arch installations. I am `dubious`_ as to the wisdom
of their specific migration strategy, but I certainly can't complain about
the vote of confidence!

The OpenStack project, likely the largest open source Python project short of
the Linux distro aggregations, is also in the process of migrating from Python
2 to Python 3, and maintains a detailed
`status tracking <https://wiki.openstack.org/wiki/Python3>`__
page for the migration.

Outside the Linux ecosystem, other Python redistributors like ActiveState,
Enthought, and Continuum Analytics provide both Python 2 and Python 3 releases,
and Python 3 environments are also available through the major public cloud
platforms.


.. _Python 2 or Python 3: http://wiki.python.org/moin/Python2orPython3
.. _the process of eliminating: https://wiki.ubuntu.com/Python/3
.. _late 2015: https://fedoraproject.org/wiki/Changes/Python_3_as_Default
.. _Red Hat Software Collections: http://developerblog.redhat.com/2013/09/12/rhscl1-ga/
.. _default Python: https://www.archlinux.org/news/python-is-now-python-3/
.. _dubious: http://www.python.org/dev/peps/pep-0394/


When can we expect Python 2 to be a purely historical relic?
------------------------------------------------------------

Python 2 is still a good language. While I think Python 3 is a *better*
language (especially when it comes to the text model, error reporting, the
native coroutine syntax in Python 3.5, and the string formatting syntax in
Python 3.6), we've deliberately designed the migration plan so users can update
on *their* timetable rather than ours (at least within a window of several
years), and we expect commercial redistributors to extend that timeline even
further.

The PyPy project have also stated their intention to continue providing a
Python 2.7 compatible runtime indefinitely, since the RPython language used
to implement PyPy is a subset of Python 2 rather than of Python 3.

I personally expect CPython 2.7 to remain a reasonably common deployment
platform until mid 2024. Red Hat Enterprise Linux 7 (released in June 2014)
uses CPython 2.7 as the system Python, and many library, framework and
application developers base their minimum supported version of Python on the
system Python in RHEL (especially since that also becomes the system Python in
downstream rebuilds like CentOS and Scientific Linux). While Red Hat's actively
trying to change that slow update cycle by encouraging application developers
to target the Software Collections runtimes rather than the system Python, that
change in itself is a significant cultural shift for the RHEL/CentOS user base.

Aside from Blender, it appears most publishing and animation tools with
Python support (specifically Scribus, InkScape and AutoDesk tools like
Maya and MotionBuilder) are happy enough with Python 2.7. GIS tools similarly
currently still use Python 2.7. This actually makes a fair bit of sense,
especially for the commercial tools, since the Python support in these tools is
there primarily to manipulate the application data model and there arguably
aren't any major improvements in Python 3 for that kind of use case as yet, but
still some risk of breaking existing scripts if the application updates to
Python 3.

For the open source applications when Python 2 is currently seen as a
"good enough" scripting engine, the likely main driver for Python 3 scripting
support is likely to be commercial distribution vendors looking to drop
commercial Python 2 runtime support - the up front investment in application
level Python 3 support would be intended to pay off in the form of reduced long
term sustaining engineering costs at the language runtime level.

That said, the Python 3 reference interpreter also offers quite a few new low
level configuration options that let embedding applications control the memory
allocators used, monitor and control all bytecode execution, and various
other improvements to the runtime embedding functionality, so the natural
incentives for application developers to migrate are starting to accumulate,
which means we may see more activity on that front as the 2020 date for the
end of community support of the Python 2 series gets closer.


.. _slow-uptake:

But uptake is so slow, doesn't this mean Python 3 is failing as a platform?
---------------------------------------------------------------------------

While the frequency with which this question is asked has declined markedly
since 2015 or so, a common thread I saw running through such declarations of
"failure" was people not quite understanding the key questions where the
transition plan was aiming to change the answers. These are the three key
questions:

* "I am interested in learning Python. Should I learn Python 2 or Python 3?"
* "I am teaching a Python class. Should I teach Python 2 or Python 3?"
* "I am an experienced Python developer starting a new project. Should I
  use Python 2 or Python 3?"

At the start of the migration, the answer to all of those questions was
*obviously* "Python 2". By August 2015, I considered the answer to be
"Python 3.4, unless you have a compelling reason to choose Python 2 instead".
Possible compelling reasons included "I am using existing course material
that was written for Python 2", "I am teaching the course to maintainers
of an existing Python 2 code base", "We have a large in-house collection of
existing Python 2 only support libraries we want to reuse" and "I only use
the version of Python provided by my Linux distro vendor and they currently
only support Python 2" (in regards to that last point, we realised early that
the correct place to tackle it was on the *vendor* side, and by late 2014,
all of Canonical, Red Hat, and SUSE had commercial Python 3 offerings
available).

Note the question that *isn't* on the list: "I have a large Python 2
application which is working well for me. Should I migrate it to Python 3?".

While OpenStack and some key Linux distributions have answered "Yes", for most
organisations the answer to *that* question remained "No" for several years
while companies like Canonical, Red Hat, Facebook, Google, Dropbox, and others
worked to migrate their own systems, and published the related migration
tools (such as the ``pylint --py3k`` option, and the work that has gone into the
``mypy`` and ``typeshed`` projects to allow Python 3 static type analysis to be
applied to Python 2 programs prior to attempting to migrate them).

While platform effects are starting to shift even the answer to that question
towards "Maybe" for the majority of users (and Python 3 gives Python 2 a much
nicer exit strategy to a newer language than COBOL ever did), the time frame
for *that* change is a lot longer than the five years that was projected for
changing the default choice of Python version for green field projects.

That said, reducing or eliminating any major remaining barriers to migration
is an ongoing design goal for Python 3.x releases, at least in those cases
where the change is also judged to be an internal improvement within Python 3
(for example, the restoration of binary interpolation support in Python 3.5 was
motivated not just by making it easier to migrate from Python 2, but also to
make certain kinds of network programming and other stream processing code
easier to write in Python 3).

In the earlier days of the Python 3 series, several of the actions taken by
the core development team were actually deliberately designed to keep
conservative users *away* from Python 3 as a way of providing time for the
ecosystem to mature.

Now, if Python 3 had failed to offer a desirable platform, nobody would have
cared about this in the slightest. Instead, what we saw was the following:

* people coming up with great migration guides and utilities *independently*
  of the core development team. While `six`_ was created by a core
  developer (Benjamin Peterson), and ``lib2to3`` and the main porting guides
  are published by the core development team, `python-modernize`_ was created
  by Armin Ronacher (creator of Jinja2 and Flask), while `python-future`_
  was created by Ed Schofield based on that earlier work. Lennart Regebro
  has also done stellar work in creating an `in-depth guide to porting to
  Python 3 <http://python3porting.com/>`__
* Linux distributions aiming to make Python 2 an optional download and
  have only Python 3 installed by default
* commercial Python redistributors and public cloud providers ensuring that
  Python 3 was included as one of their supported offerings
* customers approaching operating system vendors and asking for assistance
  in migrating large proprietary code bases from Python 2 to Python 3
* more constrained plugin ecosystems that use an embedded Python interpreter
  (like Blender, gcc, and gdb) either adding Python 3 support, or else
  migrating entirely from Python 2 to 3
* developers lamenting the fact that they *wanted* to use Python 3, but were
  being blocked by various dependencies being missing, or because they
  previously used Python 2, and needed to justify the cost of migration to
  their employer
* library and framework developers that hadn't already added Python 3 support
  for their own reasons being strongly encouraged by their users to offer it
  (sometimes in the form of code contributions, other times in the form of
  tracker issues, mailing list posts and blog entries)
* interesting new implementations/variants like MyPy and MicroPython taking
  advantage of the removal of legacy behaviour to target the leaner Python 3
  language design rather than trying to handle the full backwards
  compatibility implications of implementing Python 2
* developers complaining that the core development team wasn't being
  aggressive enough in forcing the community to migrate promptly rather than
  allowing the migration to proceed at its own pace (!)

That last case only appeared around 2014 (~5 years into the migration), and
the difference in perspective appears to be an instance of the classic early
adopter/early majority divide in platform adoption. The deliberately gentle
migration plan was (and is) for the benefit of the late adopters that drive
Python's overall popularity, not the early adopters that make up both the open
source development community and the (slightly) broader software development
blogging community.

It's important to keep in mind that Python 2.6 (released October 2008) has long
stood as one of the most widely deployed versions of Python, purely through
being the system Python in Red Hat Enterprise Linux 6 and its derivatives,
and usage of Python 2.4 (released November 2004) remained non-trivial through to
at least March 2017 for the same reason with respect to Red Hat Enterprise
Linux 5.

I expect there is a similar effect from stable versions of Debian, Ubuntu LTS
releases and SUSE Linux Enterprise releases, but (by some strange coincidence)
I'm not as familiar with the Python versions and end-of-support dates for those
as I am with those for the products sold by my employer ;)

If we weren't getting complaints from the early adopter crowd about the pace
of the migration, *then* I would have been worried (as it would have indicated
they had abandoned Python entirely and moved on to something else).

The final key point to keep in mind is that the available metrics on Python
3 adoption are quite limited, and that remains true regardless of whether we
think the migration is going well or going poorly. The three main quantitative
options are to analyse user agents on the Python Package Index, declarations
of Python 3 support on PyPI and binary installer downloads for Mac OS X and
Windows from python.org.

The first of those remains heavily dominated by *existing* Python 2 users, but
the trend in Python 3 usage is still upwards. These metrics are stored as a
public data set in Google Big Query, and
`this post <https://langui.sh/2016/12/09/data-driven-decisions/>`__ goes over
some of the queries that are possible with the available data. The records
are incomplete prior to June 2016, but running the query in April 2017 shows
downloads from Python 3 clients increasing from around 7% of approximately 430
million downloads in June 2016 to around 12% of approximately 720 million
downloads in March 2017.

The second is based on publisher provided package metadata rather than automated
version compatibility checking.

Of the top 360 `most downloaded packages <http://py3readiness.org/>`__, ~94%
offer Python 3 support, with several of those that are Python 2 only (such as
graphite-web and supervisord) typically being run as standalone services rather
than as imported modules that necessarily need to be using the same version of
Python. Again, the trend is upwards (the number in 2014 was closer to 70%),
and I'm not aware of anyone *adding* Python 3 support, and then removing it as
imposing too much maintenance overhead.

The last metric reached the point where Python 3 downloads outnumbered Python 2
downloads (54% vs 46%) back in 2013. Those stats needs to be collected manully
from the ``www.python.org`` server access logs, so I don't have anything more
recent than that.

The Python 3 ecosystem is definitely still the smaller of the two as of April
2017 (by a non-trivial margin), but users that start with Python 3 are able
to move parts of their applications and services to Python 2 readily enough if
the need arises, and hopefully with a clear idea of which parts of Python 2 are
the modern recommended parts that survived the transition to Python 3, and which
parts are the legacy cruft that only survives in the latest Python 2.x releases
due to backwards compatibility concerns.

For the inverse question relating to the concern that the existing migration
plan is too *aggressive*, see :ref:`abandoning-users`.


Is the ultimate success of Python 3 as a platform assured?
----------------------------------------------------------

Yes, its place as the natural successor to the already dominant Python 2
platform is now assured. Commercial support has long been available from
multiple independent vendors, the vast majority of the core components from the
Python 2 ecosystem are already available, and the combination of the Python
3.5+ releases and Python's uptake in the education and data analysis sectors
provide assurance of a steady supply of both Python developers, and work for
those developers (in the 2016 edition of IEEE's survey of programming languages,
Python was 3rd, trailing only Java and C, overtaking C++ relative to its
2015 position, and both C++ and C# relative to the initial 2014 survey).

For me, with my Linux-and-infrastructure-software bias, the
tipping point has been Ubuntu and Fedora successfully making the transition
to only having Python 3 in their default install. That change means that
a lot of key Linux infrastructure software is now Python 3 compatible, as
well as representing not only a significant statement of trust in the Python 3
platform by a couple of well respected organisations (Canonical and Red Hat),
but also a non-trivial investment of developer time and energy in performing
the migration. This change will also mean that Python 3 will be more readily
available than Python 2 on those platforms in the future, and hence more likely
to be used as the chosen language variant for Python utility scripts, and hence
increase the attractiveness of supporting Python 3 for library and framework
developers.

A significant milestone only attained over 2016 and 2017 has been the three
largest public cloud providers (Amazon Web Services, Microsoft Azure, and
Google Cloud Platform) ensuring that Python 3 is a fully supported development
option on their respective platforms, adding to the support already previously
available in platforms like Heroku and OpenShift Online.

Specifically in the context of infrastructure, I also see the `ongoing migration
<https://wiki.openstack.org/wiki/Python3>`__ of OpenStack components from
being Python 2 only applications to being Python 3 compatible as highly
significant, as OpenStack is arguably one of the most notable Python
projects currently in existence in terms of spreading awareness outside
the traditional open source and academic environs. In particular, as
OpenStack becomes a Python 3 application, then the plethora of regional cloud
provider developers and hardware vendor plugin developers employed
to work on it will all be learning Python 3 rather than Python 2.

A notable early contribution to adoption has been the education community's
staunch advocacy for the wider Python community to catch up with them in
embracing Python 3, rather than confusing their students with occasional
recommendations to learn Python 2 directly, rather than learning Python 3
first.

As far as the scientific community goes, they were amongst the earliest
adopters of Python 3 - I assume the reduced barriers to learnability were
something they appreciated, and the Unicode changes were not a problem that
caused them significant trouble.

I think the web development community has certainly had the roughest time of
it. Not only were the WSGI update discussions long and drawn out (and as
draining as any standards setting exercise), resulting in a compromise
solution that at least works but isn't simple to deal with, but they're also
the most directly affected by the additional challenges faced when working
directly with binary data in Python 3. However, even in the face of these
issues, the major modern Python web frameworks, libraries and database
interfaces *do* support Python 3, and the return of binary interpolation
support in Python 3.5 addressed some of the key concerns raised by the
developers of the Twisted networking library.

The adoption of ``asyncio`` as *the* standard framework for asynchronous IO and
the subsequent incorporation of first class syntactic support for coroutines
have also helped the web development community resolve a long standing issue
with a lack of a standard way for web servers and web frameworks to communicate
regarding long lived client connections (such as those needed for WebSockets
support), providing a clear incentive for migration to Python 3.3+ that
didn't exist with earlier Python 3 versions.


Python 3 is meant to make Unicode easier, so why is <X> harder?
---------------------------------------------------------------

As of 2015, the Python community as a whole had had more than 15 years
to get used to the Python 2 way of handling Unicode. By contrast, for Python 3,
we'd only had a production ready release available for just over 5 years,
and since some of the heaviest users of Unicode are the web
framework developers, and they'd only had a stable WSGI target since the
release of 3.2, you could drop that down to just under 5 years of intensive
use by a wide range of developers with extensive practical experiencing
in handling Unicode (we have some *excellent* Unicode developers in the
core team, but feedback from a variety of sources is invaluable for a
change of this magnitude).

That feedback has already resulted in major improvements in the Unicode
support for the Python 3.2, 3.3, 3.4, 3.5, and 3.6 releases. With the
``codecs`` and ``email`` modules being brought into line, the Python 3.4
release was the first one where the transition felt close to
being "done" to me in terms of coping with the full implications of a
strictly enforced distinction between binary and text data in the standard
library, while Python 3.5 revisited some of the earlier design decisions of
the Python 3 series and changed some of them based on several years of
additional experience. Python 3.6 brought some major changes to the way
binary system APIs are handled on Windows, and changes of similar scope are
anticipated for 3.7 on non-Windows systems.

While I'm optimistic that the system boundary handling changes proposed for
Python 3.7 will resolve the last of the major issues, I nevertheless expect
that feedback process will continue throughout the 3.x series, since "mostly
done" and "done" aren't quite the same thing, and attempting to closely
integrate with POSIX systems that may be using ASCII incompatible encodings
while using a text model with strict binary/text separation hasn't really
been done before at Python's scale (the JVM is UTF-16 based, but bypasses
most OS provided services, while other tools often choose the approach of
just assuming that all bytes are UTF-8 encoded, regardless of what the
underlying OS claims).

In addition to the cases where blurring the binary/text distinction really
did make things simpler in Python 2, we're also forcing even developers in
strict ASCII-only environments to have to care about Unicode correctness,
or else explicitly tell the interpreter not to worry about it. This means
that Python 2 users that may have previously been able to ignore Unicode
issues may need to account for them properly when migrating to Python 3.

I've written more extensively on both of these topics in
:ref:`binary-protocols` and :ref:`py3k-text-files`, while :pep:`538` and
:pep:`540` go into detail on the system boundary changes now being proposed
for Python 3.7.


Python 3 is meant to fix Unicode, so why is <X> still broken?
-------------------------------------------------------------

The long march from the early assumptions of Anglocentric ASCII based
computing to a more global Unicode based future is still ongoing, both for
the Python community, and the computing world at large. Computers are still
generally much better at dealing with English and other languages with
similarly limited character sets than they are with the full flexibility of
human languages, even the subset that has been pinned down to a particular
binary representation thanks to the efforts of the Unicode Consortium.

While the changes to the core text model in Python 3 *did* implicitly address
many of the Unicode issues affecting Python 2, there are still plenty of
Unicode handling issues that require their own independent updates. For
example, the interactive console on Windows poses some particular challenges
that have `yet to be satisfactorily resolved
<http://bugs.python.org/issue1602>`__. One recurring problem is that many
of these are relatively easy to work around (such as by using a graphical
environment rather than the default interactive interpreter to avoid the
command line limitations on Windows), but comparatively hard to fix properly
(and then get agreement that the proposed fix is a suitable one).

The are also more specific questions covering the state of the :ref:`WSGI
middleware interface <wsgi-status>` for web services, and the issues that
can arise when dealing with :ref:`posix-systems`.

..
   extra label to preserve link for the old question phrasing

.. _why-is-python-3-considered-a-better-language-to-teach-beginning-programmers:

Is Python 3 a better language to teach beginning programmers?
-------------------------------------------------------------

I believe so, yes, especially if teaching folks that aren't native English
speakers. However, I also expect a lot of folks will still
want to continue on and learn Python 2 even if they learn Python 3 first
- I just think that for people that don't already know C, it will be
easier to start with Python 3, and then learn Python 2 (and the relevant
parts of C) in terms of the differences from Python 3 rather than
learning Python 2 directly and having to learn all those legacy details
at the same time as learning to program in the first place.

.. note:: This answer was written for Python 3.5. For Python 3.6, other
   potential benefits in teaching beginners include the new f-string
   formatting syntax, the secrets module, the ability to include underscores
   to improve the readability of long numeric literals, and the ordering of
   arbitrary function keyword arguments reliably matching the order in which
   they're supplied to the function call.

As noted above, Python 2 has some interesting quirks due to its C heritage
and the way the language has evolved since Guido first created Python in
1991. These quirks then have to be taught to *every* new Python user so
that they can avoid them. The following are examples of such quirks that
are easy to demonstrate in an interactive session (and resist the temptation
to point out that these can all be worked around - for teaching beginners,
it's the default behaviour that matters, not what experts can instruct the
interpreter to do with the right incantations elsewhere in the program).

You can get unexpected encoding errors when attempting to decode values and
unexpected decoding errors when attempting to encode them, due to the
presence of decode and encode methods on both ``str`` and ``unicode``
objects, but more restrictive input type expectations for the underlying
codecs that then trigger the implicit *ASCII* based encoding or decoding::

    >>> u"\xe9".decode("utf-8")
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/usr/lib64/python2.7/encodings/utf_8.py", line 16, in decode
        return codecs.utf_8_decode(input, errors, True)
    UnicodeEncodeError: 'ascii' codec can't encode character u'\xe9' in position 0: ordinal not in range(128)
    >>> b"\xe9".encode("utf-8")
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    UnicodeDecodeError: 'ascii' codec can't decode byte 0xe9 in position 0: ordinal not in range(128)

Python 2 has a limited and inconsistent understanding of character sets
beyond those needed to record English text::

    >>> è = 1
      File "<stdin>", line 1
        è = 1
        ^
    SyntaxError: invalid syntax
    >>> print("è")
    è

That second line usually works in the interactive interpreter, but won't work
by default in a script::

    $ echo 'print("è")' > foo.py
    $ python foo.py
      File "foo.py", line 1
    SyntaxError: Non-ASCII character '\xc3' in file foo.py on line 1, but no encoding declared; see http://www.python.org/peps/pep-0263.html for details

The handling of Unicode module names is also inconsistent::

    $ echo "print(__name__)" > è.py
    $ python -m è
    __main__
    $ python -c "import è"
      File "<string>", line 1
        import è
               ^
    SyntaxError: invalid syntax

Beginners are often surprised to find that Python 2 can't do basic
arithmetic correctly::

    >>> 3 / 4
    0

Can be bemused by the fact that Python 2 interprets numbers strangely
if they have a leading zero::

    >>> 0777
    511

And may also eventually notice that Python 2 has two different kinds of
integer::

    >>> type(10) is type(10**100)
    False
    >>> type(10) is type(10L)
    False
    >>> 10
    10
    >>> 10L
    10L

The ``print`` statement is weirdly different from normal function calls::

    >>> print 1, 2, 3
    1 2 3
    >>> print (1, 2, 3)
    (1, 2, 3)
    >>> print 1; print 2; print 3
    1
    2
    3
    >>> print 1,; print 2,; print 3
    1 2 3
    >>> import sys
    >>> print >> sys.stderr, 1, 2, 3
    1 2 3

And the ``exec`` statement also differs from normal function calls like
``eval`` and ``execfile``::

    >>> d = {}
    >>> exec "x = 1" in d
    >>> d["x"]
    1
    >>> d2 = {"x":[]}
    >>> eval("x.append(1)", d2)
    >>> d2["x"]
    [1]
    >>> with open("example.py", "w") as f:
    ...     f.write("x = 1\n")
    ...
    >>> d3 = {}
    >>> execfile("example.py", d3)
    >>> d3["x"]
    1

The ``input`` builtin has some seriously problematic default behaviour::

    >>> input("This is dangerous: ")
    This is dangerous: __import__("os").system("echo you are in trouble now")
    you are in trouble now
    0

The ``open`` builtin doesn't handle non-ASCII files correctly (you have to
use ``codecs.open`` instead), although this often isn't obvious on POSIX
systems (where passing the raw bytes through the way Python 2 does often
works correctly).

You need parentheses to catch multiple exceptions, but forgetting that is
an error that passes silently::

    >>> try:
    ...   1/0
    ... except TypeError, ZeroDivisionError:
    ...     print("Exception suppressed")
    ...
    Traceback (most recent call last):
      File "<stdin>", line 2, in <module>
    ZeroDivisionError: integer division or modulo by zero
    >>> try:
    ...     1/0
    ... except (TypeError, ZeroDivisionError):
    ...     print("Exception suppressed")
    ...
    Exception suppressed

And if you make a mistake in an error handler, you'll lose the original
error::

    >>> try:
    ...     1/0
    ... except Exception:
    ...     logging.exception("Something went wrong")
    ...
    Traceback (most recent call last):
      File "<stdin>", line 4, in <module>
    NameError: name 'logging' is not defined

Python 2 also presents users with a choice between two relatively
unattractive alternatives for calling up to a parent class implementation
from a subclass method::

    class MySubclass(Example):

        def explicit_non_cooperative(self):
            Example.explicit_non_cooperative(self)

        def explicit_cooperative(self):
            super(MySubclass, self).explicit_cooperative()

List comprehensions are one of Python's most popular features, yet they
can have surprising side effects on the local namespace::

    >>> i = 10
    >>> squares = [i*i for i in range(5)]
    >>> i
    4

Python 2 is still a good language despite these flaws, but users that are
happy with Python 2 shouldn't labour under the misapprehension that the
language is perfect. We have made mistakes, and Python 3 came about because
Guido and the rest of the core development team finally became tired of
making excuses for those limitations, and decided to start down the long
road towards fixing them instead.

All of the above issues have been addressed by backwards incompatible
changes in Python 3. Once we had made that decision, then adding other
new features *twice* (once to Python 3 and again to Python 2) imposed
significant additional development effort, although we *did* do so for a
number of years (the Python 2.6 and 2.7 releases were both developed in
parallel with Python 3 releases, and include many changes originally created
for Python 3 that were backported to Python 2 since they were backwards
compatible and didn't rely on other Python 3 only changes like the new,
more Unicode friendly, IO stack).

I'll give several examples below of how the above behaviours have changed in
Python 3 releases, up to and including Python 3.6 (since that's the currently
released version).

In Python 3, the codec related builtin convenience methods are *strictly*
reserved for use with text encodings. Accordingly, text objects no longer
even have a ``decode`` method, and binary types no longer have an ``encode``
method::

    >>> u"\xe9".decode("utf-8")
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AttributeError: 'str' object has no attribute 'decode'
    >>> b"\xe9".encode("utf-8")
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AttributeError: 'bytes' object has no attribute 'encode'

In addition to the above changes, Python 3.4 included `additional changes
to the codec system
<http://docs.python.org/dev/whatsnew/3.4.html#codec-handling-improvements>`__
to help with more gently easing users into the idea that there are different
kinds of codecs, and only some of them are text encodings. It also updates
many of the networking modules to make secure connections much simpler.

Python 3 also has a much improved understanding of character sets beyond
English::

    >>> è = 1
    >>> è
    1

And this improved understanding extends to the import system::

    $ echo "print(__name__)" > è.py
    $ python3 -m è
    __main__
    $ python3 -c "import è"
    è

Python 3 has learned how to do basic arithmetic, replaces the surprising C
notation for octal numbers with the more explicit alternative supported
since Python 2.6 and only has one kind of integer::

    >>> 3 / 4
    0.75
    >>> 0777
      File "<stdin>", line 1
        0777
           ^
    SyntaxError: invalid token
    >>> 0o777
    511
    >>> type(10) is type(10**100)
    True
    >>> 10
    10
    >>> 10L
      File "<stdin>", line 1
        10L
          ^
    SyntaxError: invalid syntax

``print`` is now just an ordinary function that accepts keyword arguments,
rather than having its own custom (and arcane) syntax variations (note
that controlling the separator between elements is a feature that
requires preformatting of the string to be printed in Python 2 but was
trivial to add direct support for when print was converted to an ordinary
builtin function rather than being a separate statement)::

    >>> print 1, 2, 3
      File "<stdin>", line 1
        print 1, 2, 3
              ^
    SyntaxError: invalid syntax
    >>> print(1, 2, 3)
    1 2 3
    >>> print((1, 2, 3))
    (1, 2, 3)
    >>> print(1); print(2); print(3)
    1
    2
    3
    >>> print(1, 2, 3, sep="\n")
    1
    2
    3
    >>> print(1, end=" "); print(2, end=" "); print(3)
    1 2 3
    >>> import sys
    >>> print(1, 2, 3, file=sys.stderr)
    1 2 3


``exec`` is now more consistent with ``execfile``::

    >>> d = {}
    >>> exec("x=1", d)
    >>> d["x"]
    1

Converting ``print`` and ``exec`` to builtins rather than statements means
they now also work natively with utilities that require real function
objects (like ``map`` and ``functools.partial``), they can be replaced
with mock objects when testing and they can be more readily substituted
with alternative interfaces (such as replacing raw print statements with a
pretty printer or a logging system). It also means they can be passed to
the builtin ``help`` function without quoting, the same as other builtins.

The ``input`` builtin now has the much safer behaviour that is provided as
``raw_input`` in Python 2::

    >>> input("This is no longer dangerous: ")
    This is no longer dangerous: __import__("os").system("echo you have foiled my cunning plan")
    '__import__("os").system("echo you have foiled my cunning plan")'

The entire IO stack has been rewritten in Python 3 to natively handle
Unicode and (in the absence of system configuration errors), to favour
UTF-8 by default rather than ASCII. Unlike Python 2, :func:`open` in Python 3
natively supports ``encoding`` and ``errors`` arguments, and the
:func:`tokenize.open` function automatically handles Python source file
encoding cookies.

Failing to trap an exception is no longer silently ignored::

    >>> try:
    ...     1/0
    ... except TypeError, ZeroDivisionError:
      File "<stdin>", line 3
        except TypeError, ZeroDivisionError:
                        ^
    SyntaxError: invalid syntax

And most errors in exception handlers will now still report the original
error that triggered the exception handler::

    >>> try:
    ...     1/0
    ... except Exception:
    ...     logging.exception("Something went wrong")
    ...
    Traceback (most recent call last):
      File "<stdin>", line 2, in <module>
    ZeroDivisionError: division by zero

    During handling of the above exception, another exception occurred:

    Traceback (most recent call last):
      File "<stdin>", line 4, in <module>
    NameError: name 'logging' is not defined

Note that implicit exception chaining is the thing I miss most frequently
when working in Python 2, and the point I consider the single biggest gain
over Python 3 when migrating *existing* applications - there are few things
more irritating when debugging a rare production failure than losing the
real problem details due to a secondary failure in a rarely invoked error
path.

While you probably don't want to know how it works internally, Python 3
also provides a much cleaner API for calling up to the parent implementation
of a method::

    class MySubclass(Example):

        def implicit_cooperative(self):
            super().implicit_cooperative()

And, like generator expressions in both Python 2 and Python 3, list
comprehensions in Python 3 no longer have any side effects on the
local namespace::

    >>> i = 10
    >>> squares = [i*i for i in range(5)]
    >>> i
    10

The above improvements are all changes that *couldn't* be backported to a
hypothetical Python 2.8 release, since they're backwards incompatible with
some (but far from all) existing Python 2 code, mostly for obvious reasons.
The exception chaining isn't obviously backwards incompatible, but still
can't be backported due to the fact that handling the implications of
creating a reference cycle between caught exceptions and the execution
frames referenced from their tracebacks involved changing the lifecycle
of the variable named in an "as" clause of an exception handler (to break
the cycle, those names are automatically deleted at the end of the relevant
exception handler in Python 3 - you now need to bind the exception to a
different local variable name in order to keep a valid reference after
the handler has finished running). The list comprehension changes are also
backwards incompatible in non-obvious ways (since not only do they no
longer leak the variable, but the way the expressions access the containing
scope changes - they're now full closures rather than running directly
in the containing scope).

As documented in :pep:`466`, the networking security changes were deemed
worthy of backporting. In contrast, while it's perhaps *possible* to backport
the implicit super change, it would need to be separated from the other
backwards incompatible changes to the type system machinery (and in that
case, there's no "help improve the overall security of the internet" argument
to be made in favour of doing the work).

There are some other notable changes in Python 3 that are of substantial
benefit when teaching new users (as well as for old hands), that technically
*could* be included in a Python 2.8 release if the core development chose to
create one, but in practice such a release isn't going to happen. However,
folks interested in that idea may want to check out the `Tauthon project`_,
which is a Python 2/3 hybrid language that maintains full Python 2.7
compatibility while backporting backwards compatible enhancement from the
Python 3 series.

.. _Tauthon project: https://github.com/naftaliharris/tauthon

:pep:`3151` means that Python 3.3+ has a significantly more sensible system
for catching particular kinds of operating system errors. Here's the race
condition free way to detect a missing file in Python 2.7:

    >>> import errno
    >>> try:
    ...     f = open("This does not exist")
    ... except IOError as err:
    ...     if err.errno != errno.ENOENT:
    ...         raise
    ...     print("File not found")
    ...
    File not found

And here's the same operation in Python 3.3+::

    >>> try:
    ...     f = open("This does not exist")
    ... except FileNotFoundError:
    ...     print("File not found")
    ...
    File not found

(If you're opening the file for writing, then you can use
`exclusive mode
<http://docs.python.org/3/whatsnew/3.3.html#builtin-functions-and-types>`__
to prevent race conditions without using a subdirectory - Python 2 has no
equivalent. There are many other cases where Python 3 exposes operating
system level functionality that wasn't broadly available when the feature
set for Python 2.7 was frozen in April 2010).

Another common complaint with Python 2 is the requirement to use empty
``__init__.py`` files to indicate a directory is a Python package, and the
complexity of splitting a package definition across multiple directories.
By contrast, here's an example of how to split a package across multiple
directories in Python 3.3+ (note the lack of ``__init__.py`` files). While
technically this can be backported, the implementation depends on the new
pure Python implementation of the import system, which in turn depends on
the Unicode friendly IO stack in Python 3, so backporting it is far
from trivial::

    $ mkdir -p dir1/nspkg
    $ mkdir -p dir2/nspkg
    $ echo 'print("Imported submodule A")' > dir1/nspkg/a.py
    $ echo 'print("Imported submodule B")' > dir2/nspkg/b.py
    $ PYTHONPATH=dir1:dir2 python3 -c "import nspkg.a, nspkg.b"
    Imported submodule A
    Imported submodule B

That layout doesn't work at all in Python 2 due to the missing
``__init__.py`` files, and even if you add them, it still won't find
the second directory::

    $ PYTHONPATH=dir1:dir2 python -c "import nspkg.a, nspkg.b"
    Traceback (most recent call last):
      File "<string>", line 1, in <module>
    ImportError: No module named nspkg.a
    $ touch dir1/nspkg/__init__.py
    $ touch dir2/nspkg/__init__.py
    $ PYTHONPATH=dir1:dir2 python -c "import nspkg.a, nspkg.b"
    Imported submodule A
    Traceback (most recent call last):
      File "<string>", line 1, in <module>
    ImportError: No module named b

That last actually shows another limitation in Python 2's error handling
since import failures don't always show the full name of the missing
module. That is fixed in Python 3::

    $ PYTHONPATH=dir1 python3 -c "import nspkg.a, nspkg.b"
    Imported submodule A
    Traceback (most recent call last):
      File "<string>", line 1, in <module>
    ModuleNotFoundError: No module named 'nspkg.b'

That said: Eric Snow *has* now backported the Python 3.4 import system
to Python 2.7 as `importlib2 <https://pypi.python.org/pypi/importlib2>`__.
I'm aware of at least one large organisation using that in production and
being quite happy with the results :)

Python 3.3 also included some `minor <http://bugs.python.org/issue12265>`__
`improvements <http://bugs.python.org/issue12356>`__ to the error messages
produced when functions and methods are called with incorrect arguments.


Out of the box, why is Python 3 better than Python 2?
-----------------------------------------------------

The feature set for Python 2.7 was essentially locked in April 2010 with the
first beta release. Since then, with a very limited number of exceptions
related to network security, the Python core development team have only been
adding new features directly to the Python 3 series. These new features are
informed both by our experience with Python 3 itself, as well as with our
ongoing experience working with Python 2 (as they're still very similar
languages).

As Python 2 is a mature, capable language, with a rich library of support
modules available from the Python Package Index (including many backports
from the Python 3 standard library), there's no one universally important
feature that will provide a compelling argument to switch for *existing*
Python 2 users. Of necessity, existing Python 2 users are those who
didn't find the limitations of Python 2 that lead to the creation of Python
3 particularly problematic. It is for the benefit of these users that Python
2 continues to be maintained.

For *new* users of Python however, Python 3 represents years of additional
work above and beyond what was included in the Python 2.7 release. Features
that may require third party modules, or simply not be possible at all in
Python 2, are provided by default in Python 3. This answer doesn't attempt
to provide an exhaustive list of such features, but does aim to provide an
illustrative overview of the kinds of improvements that have been made.
The `What's New <http://docs.python.org/3/whatsnew/>`__ guides for the
Python 3 series (especially the 3.3+ releases that occurred after the
Python 2 series was placed in long term maintenance) provide more
comprehensive coverage.

While I've tried to just hit some highlights in this list, it's still rather
long. The full What's New documents are substantially longer.

.. note:: This answer was written for Python 3.5. For Python 3.6, some other
   notable enhancements include the new f-string formatting syntax, the secrets
   module, the ability to include underscores to improve the readability of
   long string literals, changes to preserve the order of class namespaces
   and function keyword arguments, type hints for named variables, and more.

Some changes that are likely to affect most projects are error handling
related:

* the exception hierarchy for operating system errors is now based on what
  went wrong, rather than which module detected the failure (see :pep:`3151`
  for details).
* bugs in error handling code no longer hide the original exception (which
  can be a huge time saver when it happens to hard to reproduce bugs)
* by default, if the logging system is left unconfigured, warnings and
  above are written to sys.stderr, while other events are ignored
* the codec system endeavours to ensure the codec name always appears in the
  reported error message when the underlying call fails
* the error messages from failed argument binding now do a much better job
  of describing the expected signature of the function
* the socket module takes advantage of the new enum support to include
  constant names (rather than just numeric values) in the error message
  output
* starting in Python 3.5, all standard library modules making system calls
  should handle EINTR automatically

Unicode is more deeply integrated into the language design, along with a
clearer separation between binary and text data:

* the :func:`open` builtin natively supports decoding of text files (rather
  than having to use :func:`codecs.open` instead)
* the ``bytes`` type provides locale independent manipulation of binary data
  that may contain ASCII segments (the Python 2 ``str`` type has locale
  dependent behaviour for some operations)
* the codec system has been separated into two tiers. The :meth:`str.encode`,
  :meth:`bytes.decode` and :meth:`bytearray.decode` methods provide direct
  access to Unicode text encodings, while the :mod:`codecs` module provides
  general access to all available codecs, including binary->binary and
  text->text transforms (in Python 2, all three kinds can be accessed through
  the convenience methods on the builtin types, creating ambiguity as to the
  expected return types of the affected methods)
* data received from the operating system is automatically decoded to text
  whenever possible (this does cause integration issues in some cases when
  the OS provides incorrect configuration data, but otherwise allows
  applications to ignore more cross-platform differences in whether OS APIs
  natively use bytes or UTF-16)
* identifiers and the import system are no longer limited to ASCII text
  (allowing non-English speakers to use names in their native languages
  when appropriate)
* Python 3 deliberately has no equivalent to the implicit ASCII based
  decoding that takes place in Python 2 when an 8-bit ``str`` object
  encounters a ``unicode`` object (note that disabling this implicit
  conversion in Python 2, while technically possible, is not typically
  feasible, as turning it off breaks various parts of the standard library)
* Python 3.3+ now correctly handles code points outside the basic
  multilingual plane without needing to use 4 bytes per code point for all
  Unicode data (as Python 2 does)

A few new debugging tools are also provided out of the box:

* :mod:`faulthandler` allows the generation of Python tracebacks for
  segmentation faults and threading deadlocks (including a
  ``-X faulthandler`` command line option to debug arbitrary scripts)
* :mod:`tracemalloc` makes it possible to track where objects were
  allocated and obtain a traceback summary for those locations (this relies
  on the dynamic memory allocator switching feature added in Python 3.4 and
  hence cannot be backported to Python 2 without patching the interpreter
  and building from source
* the :mod:`gc` module now provides additional introspection and hook APIs

The concurrency support has been improved in a number of ways:

* The native coroutine syntax added in Python 3.5 is substantially more
  approachable than the previous "generators-as-coroutines" syntax (as it
  avoids triggering iterator based intuitions that aren't actually helpful in
  the coroutine case)
* :mod:`asyncio` (and the supporting :mod:`selectors` module) provides
  greatly enhanced native support for asynchronous IO
* :mod:`concurrent.futures` provides straightforward support for dispatching
  work to separate working processes or threads
* :mod:`multiprocessing` is far more configurable (including the option to
  avoid relying on ``os.fork`` on POSIX systems, making it possible to avoid
  the poor interactions with between threads and ``os.fork``, while still
  using both multiple processes and threads)
* the CPython Global Interpreter Lock has been updated to switch contexts
  based on absolute time intervals, rather than by counting bytecode
  execution steps (context switches will still occur between bytecode
  boundaries)

For data analysis use cases, there's one major syntactic addition:

* Python 3.5 added a new binary operator symbol specifically for use in matrix
  multiplication

Notable additions to the standard library's native testing capabilities
include:

* the :mod:`unittest.mock` module, previously only available as a third party
  library
* a "subtest" feature that allows arbitrary sections of a test to be reported
  as independent results (including details on what specific values were
  tested), without having to completely rewrite the test to fit into a
  parameterised testing framework
* a new ``FAIL_FAST`` option for :mod:`doctest` that requests stopping the
  doctest at the first failing test, rather than continuing on to run the
  remaining tests

Performance improvements include:

* significant optimisation work on various text encodings, especially UTF-8,
  UTF-16 and UTF-32
* a significantly more memory efficient Unicode representation, especially
  compared to the unconditional 4 bytes per code point used in Linux distro
  builds of Python 2
* a C accelerator module for the :mod:`decimal` module
* transparent use of other C accelerator modules where feasible (including
  for :mod:`pickle` and :mod:`io`)
* the :class:`range` builtin is now a memory efficient calculated sequence
* the use of iterators or other memory efficient representations for various
  other builtin APIs that previously returned lists
* dictionary instances share their key storage when possible, reducing the
  amount of memory consumed by large numbers of class instances
* the rewritten implementation of the import system now caches directory
  listings for a brief time rather than blindly performing ``stat``
  operations for all possible file names, drastically improving startup
  performance when network filesystems are present on ``sys.path``

Security improvements include:

* support for "exclusive mode" when opening files
* support for the directory file descriptor APIs that avoid various symlink
  based attacks
* switching the default hashing algorithm for key data types to SIPHash
* providing an "isolated mode" command line switch to help ensure user
  settings don't impact execution of particular commands
* disabling inheritance of file descriptors and Windows handles by child
  processes by default
* new multiprocessing options that avoid sharing memory with child process
  by avoiding the ``os.fork`` system call
* significant improvements to the SSL module, such as TLS v1.1 and v1.2
  support, Server Name Indication support, access to platform certificate
  stores, and improved support for certificate verification (while these
  are in the process of being backported to Python 2.7 as part of :pep:`466`,
  it is not yet clear when that process will be completed, and those
  enhancements are already available in Python 3 today)
* other networking modules now take advantage of many of the SSL module
  improvements, including making it easier to use the new
  ``ssl.create_default_context()`` to choose settings that default to
  providing reasonable security for use over the public internet, rather
  maximising interoperability (but potentially allowing operation in no
  longer secure modes)

Object lifecycle and resource management has also improved significantly:

* the cyclic garbage collector is now more aggressive in attempting to
  collect cycles, even those containing ``__del__`` methods. This eliminated
  some cases where generators could be flagged as uncollectable (and hence
  effectively leak memory)
* this means most objects will now have already been cleaned up before the
  last resort "set module globals to None" step triggers during shutdown,
  reducing spurious tracebacks when cleanup code runs
* the new :func:`weakref.finalize` API makes it easier to register weakref
  callbacks without having to worry about managing the lifecycle of the
  reference itself
* many more objects in the standard library now support the context
  management protocol for explicit lifecycle and resource management

Other quality of life improvements include:

* ``__init__.py`` files are no longer needed to declare packages - if no
  ``foo/__init__.py`` file is present, then all directories named ``foo`` on
  ``sys.path`` will be automatically scanned for ``foo`` submodules
* the new ``super`` builtin makes calling up to base class method
  implementations in a way that supports multiple inheritance relatively
  straightforward
* keyword only arguments make it much easier to add optional parameters to
  functions in a way that isn't error prone or hard to read
* the ``yield from`` syntax for delegating to subgenerators and iterators
  (this is a key part of the :mod:`asyncio` coroutine support)
* iterable unpacking syntax is now more flexible
* :mod:`zipapp` for bundling pure Python applications into runnable archives
* :mod:`enum` for creating enumeration types
* :mod:`ipaddress` for working with both IPv4 and IPv6 addresses
* :mod:`pathlib` for a higher level filesystem abstraction than the low
  level interface provided by ``os.path``
* :mod:`statistics` for a simple high school level statistics library
  (mean, median, mode, variance, standard deviation, etc)
* :meth:`datetime.timestamp` makes it easy to convert a datetime object to a
  UNIX timestamp
* :func:`time.get_clock_info` and related APIs provide access to a rich
  collection of cross platform time measurement options
* :mod:`venv` provides virtual environment support out of the box, in a way
  that is better integrated with the core interpreter than is possible in
  Python 2 with only ``virtualenv`` available
* :mod:`ensurepip` ensures ``pip`` is available by default in Python 3.4+
  installations
* :class:`memoryview`` is significantly more capable and reliable
* the caching mechanism for pyc files has been redesigned to better
  accommodate sharing of Python files between multiple Python interpreters
  (whether different versions of CPython, or other implementation like PyPy
  and Jython)
* as part of that change, implicitly compiled bytecode cache files are
  written to __pycache__ directories (reducing directory clutter) and are
  ignored if the corresponding source file has been removed (avoiding obscure
  errors due to stale cached bytecode files)
* :class:`types.SimpleNamespace` and :class:`types.MappingProxyType` are
  made available at the Python layer
* improved introspection support, based on the :func:`inspect.signature` API,
  and its integration into :mod:`pydoc`, allowing accurate signature
  information to be reported for a much wider array of callables than just
  actual Python function objects
* defining ``__eq__`` without also defining ``__hash__`` implicitly disables
  hashing of instances, avoiding obscure errors when such types were added
  to dictionaries (you now get an error about an unhashable type when first
  adding an instance, rather than obscure data driven lookup bugs later)
* ordered comparisons between objects of different types are now disallowed
  by default (again replacing obscure data driven errors with explicit
  exceptions)

Some more advanced higher order function manipulation and metaprogramming
capabilities are also readily available in Python 3:

* the :func:`functools.partialmethod` function makes it straightforward to
  do partial function application in a way that still allows the instance
  object to be supplied later as a positional argument
* the :func:`functools.singledispatch` decorator makes it easy to create
  generic functions that interoperate cleanly with Python's type system,
  including abstract base classes
* the :class:`contextlib.ExitStack` class makes it easy to manipulate
  context managers dynamically, rather than having to rely on explicit
  use of with statements
* The new ``__prepare__`` method, and associated functions in the ``types``
  module makes it possible for metaclasses to better monitor what happens
  during class body execution (for example, by using an ordered dictionary
  to record the order of assignments)
* the updated import system permits easier creation of custom import hooks.
  In particular, the `"source to code"
  <https://docs.python.org/3/library/importlib.html#importlib.abc.InspectLoader.source_to_code>`__
  translation step can be overridden, while reusing the rest of the import
  machinery (including bytecode caching) in a custom import hook
* the :class:`dis.Bytecode` API and related functionality makes it easier to
  work with CPython bytecode

Various improvements in Python 3 also permitted some significant
documentation improvements relative to Python 2:

* as the Python 3 builtin sequences are more compliant with their
  corresponding abstract base classes, it has proved easier to flesh out
  their documentation to cover all the additional details that have been
  introduced since those docs were originally written
* the final removal of the remnants of the legacy import system in Python
  3.3 made it feasible to finally document the import system mechanics
  in the `language reference
  <https://docs.python.org/3/reference/import.html>`__

While many of these features *are* available in Python 2 with appropriate
downloads from the Python Package Index, not all of them are, especially
the various changes to the core interpreter and related systems.

While Python 2 does still have a longer tail of esoteric modules available
on PyPI, most popular third party modules and frameworks either support both,
have alternatives that support Python 3. or can be relatively easily ported
using tools like ``futurize``  (part of
`python-future <http://python-future.org>`__). The ``3to2`` project, and the
``pasteurize`` tool (also part of `python-future <http://python-future.org>`__)
offer options for migrating a pure Python 3 application to the large common
subset of Python 2 and Python 3 if a critical Python 2 only dependency is
identified, and it can't be invoked in a separate Python 2 process, or cost
effectively ported to also run on Python 3.

With Python 3 software collections available for both Red Hat Enterprise
Linux and CentOS, Ubuntu including a fully supported Python 3 stack in its
latest LTS release, and Continuum Analytics releasing Anaconda3 (a Python 3
based version of their scientific software distribution), the number of cases
where using Python 2 is preferable to using Python 3 is dwindling to those
where:

* for some reason, an application absolutely needs to run in the system
  Python on Red Hat Enterprise Linux or CentOS (for example, depending on an
  OS level package that isn't available from PyPI, or needing a complex
  binary dependency that isn't available for the Python 3 software collection
  and not being permitted to add additional dependencies from outside the
  distro)
* the particular application can't tolerate the current integration issues
  with the POSIX C locale or the Windows command line in environments that
  actually need full Unicode support
* there's a critical Python 2 only dependency that is known before the
  project even starts, and separating that specific component out to its own
  Python 2 process while writing the bulk of the application in Python 3
  isn't considered an acceptable architecture

.. _room-for-improvement:

Is Python 3 more convenient than Python 2 in every respect?
-----------------------------------------------------------

At this point in time, not quite. Python 3.5 comes much closer to this
than Python 3.4 (which in turn was closer than 3.3, etc), but there are
still some use cases that are more convenient in Python 2 because it handles
them by default, where Python 3 needs some additional configuration, or even
separate code paths for things that could be handled by a common algorithm in
Python 2.

In particular, many binary protocols include ASCII compatible segments,
so it is sometimes convenient to treat them as text strings. Python 2 makes
this easier in many cases, since the 8-bit ``str`` type blurs the boundary
between binary and text data. By contrast, if you want to treat binary data
like text in Python 3 in a way that isn't directly supported by the
``bytes`` type, you actually need to convert it to text first, and
make conscious decisions about encoding issues that Python 2 largely lets
you ignore. I've written a separate essay specifically about this point:
:ref:`binary-protocols`.

Python 3 also requires a bit of additional up front design work when
aiming to handle improperly encoded data. This also has its own essay:
:ref:`py3k-text-files`.

The Python 3 model also required more complex impedance matching on POSIX
platforms, which is covered by a separate question: :ref:`posix-systems`.

Until Python 3.4, the Python 3 codec system also didn't cleanly handle
the transform codecs provided as part of the standard library. Python 3.4
includes several changes to the way these codecs are handled that nudge
users towards the type neutral APIs in the codecs module when they attempt
to use them with the text encoding specific convenience methods on the
builtin types.

Another change that has yet to be fully integrated is the switch to
producing dynamic views from the ``keys``, ``values`` and ``items``
methods of dict objects. It currently isn't easy to implement fully
conformant versions of those in pure Python code, so many alternate
mapping implementations in Python 3 don't worry about doing so - they
just produce much simpler iterators, equivalent to the ``iterkeys``,
``itervalues`` and ``iteritems`` methods from Python 2.

Some of the changes in Python 3 designed for the benefit of larger
applications (like the increased use of iterators), or for improved
language consistency (like changing print to be a builtin function
rather than a statement) are also less convenient at the interactive
prompt. ``map``, for example, needs to be wrapped in a ``list`` call
to produce useful output in the Python 3 REPL, since by default it
now just creates an iterator, without actually doing any iteration. In
Python 2, the fact it combined both defining the iteration and actually
doing the iteration was convenient at the REPL, even though it often
resulted in redundant data copying and increased memory usage in actual
application code.

Having to type the parentheses when using print is mostly an irritation
for Python 2 users that need to retrain their fingers. I've personally
just trained myself to only use the single argument form (with parentheses)
that behaves the same way in both Python 2 and 3, and use string formatting
for anything more complex (or else just print the tuple when using the
Python 2 interactive prompt). However, I also `created a patch
<http://bugs.python.org/issue18788>`__ that proves it is possible to
implement a general implicit call syntax within the constraints of
CPython's parsing rules. Anyone that wishes to do so is free to take that
patch and turn it into a full PEP that proposes the addition of a
general implicit call syntax to Python 3.5 (or later). While such a PEP
would need to address the ambiguity problems noted on the tracker issues
(likely by restricting the form of the expression used in an implicit
call to only permit unqualified names), it's notable that the popular IPython
interactive interpreter already provides this kind of implicit "autocall"
behaviour by default, and many other languages provide a similar "no
parentheses, parameters as suffix" syntax for statements that consist of
a single function call.

Thanks are due especially to Armin Ronacher for describing several of these
issues in fine detail when it comes to the difficulties they pose
specifically when writing wire protocol handling code in Python 3. His
feedback has been invaluable to me (and others) in attempting to make
Python 3 more convenient for wire protocol development without reverting to
the Python 2 model that favoured wire protocol development over normal
application development (where binary data should exist only at application
boundaries and be converted to text or other structured data for internal
processing). There's still plenty of additional improvements that could be
made for Python 3.5 and later, though. Possible avenues for improvement
previously discussed on python-dev, python-ideas or the CPython issue
tracker include:

* :pep:`461` is an accepted proposal to restore support for *binary*
  interpolation that is to be source and semantically compatible for the use
  cases we actually want to support in Python 3.
* :pep:`467` is a draft proposal to clean up some of the legacy of the
  original Python 3 mutable ``bytes`` design. A related change is to better
  document the tuple-of-ints and list-of-ints behaviour of ``bytes`` and
  ``bytearray``.
* taking the internal "text encoding" marking system added in Python 3.4
  and giving either it or a more general codec type description system a
  public API for use when developing custom codecs.
* making it easier to register custom codecs (preferably making use of
  the native namespace package support added in Python 3.3).
* adding a new `error handler <http://bugs.python.org/issue22016>`__ that
  replaces surrogate escaped bytes with ``?`` characters in encoded output
* introducing a string tainting mechanism that allows strings containing
  surrogate escaped bytes to be tagged with their encoding assumption and
  information about where the assumption was introduced. Attempting to
  process strings with incompatible encoding assumptions would then report
  both the incompatible assumptions and where they were introduced.
* creating a "strview" type that uses memoryview to provide a str-like
  interface to arbitrary binary buffers containing ASCII compatible
  protocol data.


.. _wsgi-status:

What's up with WSGI in Python 3?
--------------------------------

The process of developing and updating standards can be slow, frustrating
and often acrimonious. One of the key milestones in enabling Python 3
adoption was when the web framework developers and web server developers
were able to agree on an updated WSGI 1.1 specification that at least
makes it *possible* to write WSGI applications, frameworks and middleware
that support Python 2 and Python 3 from a single source code base, even
though it isn't necessarily easy to do so correctly.

In particular, the Python 2 ``str`` type was particular well suited to
handling the "data in unknown ASCII compatible encoding" that is common
in web protocols, and included in the data passed through from the web
server to the application (and vice versa). At this point in time
(March 2014), nobody has created a type for Python 3 that is similarly
well suited to manipulating ASCII compatible binary protocol data. There
certainly wasn't any such type available for consideration when WSGI 1.1
was standardised in October 2010.

As a result, the "least bad" option chosen for those fields in the Python 3
version of the WSGI protocol was to publish them to the web application
as ``latin-1`` decoded strings. This means that applications need to treat
these fields as wire protocol data (even though they claim to be text
based on their type), encode them back to bytes as ``latin-1``
and then decode them again using the *correct* encoding (as indicated
by other metadata).

The WSGI 1.1 spec is definitely a case of a "good enough" solution winning
a battle of attrition. I'm actually hugely appreciative of the web
development folks that put their time and energy both into creating the
WSGI 1.1 specification *and* into updating their tools to support it. Like
the Python core developers, most of the web development folks weren't in
a position to use Python 3 professionally during the early years of its
development, but *unlike* most of the core developers, the kind of code they
write falls squarely into the ASCII
compatible binary protocol space where Python 3 still had some significant
ground to make up relative to Python 2 in terms of usability (although
we've also converted our share of such code, just in bringing the standard
library up to scratch).


.. _posix-systems:

What's up with POSIX systems in Python 3?
-----------------------------------------

.. note:: This answer was written for Python 3.5. See :pep:`538` and :pep:`540`
   for discussion of some key changes now being considered for Python 3.7.

The fact that the Python 2 text model was essentially the POSIX text model
with Unicode support bolted on to the side meant that interoperability
between Python 2 and even misconfigured POSIX systems was generally quite
straightforward - if the implicit decoding as ASCII never triggered (which
was likely for code that only included 8-bit strings and never explicitly
decoded anything as Unicode), non-ASCII data would silently pass through
unmodified.

One option we considered was to just assume everything was UTF-8 by default,
similar to the choice made by the Windows .NET platform, the GNOME GUI
toolkit and other systems. However, we decided that posed an unacceptable
risk of silently corrupting user's data on systems that *were* properly
configured to use an encoding other than UTF-8 (this concern was raised
primarily by contributors based in Europe and Asia).

This was a deliberate choice of attempting to be compatible with other
software on the end user's system at the cost of increased sensitivity to
configuration errors in the environment and differences in default
behaviour between environments with different configurations. There are also
current technical limitations in the reference interpreter's startup code
that force us to rely on the locale encoding claimed by the operating system
on POSIX systems.

:pep:`383` added the surrogateescape error handler to cope with the fact that
the configuration settings on POSIX systems aren't always a reliable guide to
the *actual* encoding of the data you encounter. One of the most common
causes of problems is the seriously broken default encoding for the default
locale in POSIX (due to the age of the ANSI C spec where that default is
defined, that default is ASCII rather than UTF-8). Bad default environments
and environment forwarding in ssh sessions are another source of problems,
since an environment forwarded from a client is not a reliable guide to the
server configuration, and if the ssh environment defaults to the C/POSIX
locale, it will tell Python 3 to use ASCII as the default encoding rather
than something more appropriate.

When surrogateescape was added, we considered enabling it for *every*
operating system interface by default (including file I/O), but the point
was once again made that this idea posed serious risks for silent data
corruption on Asian systems configured to use Shift-JIS, ISO-2022, or
other ASCII-incompatible encodings (European users were generally in a
safer position on this one, since Europe has substantially lower usage of
ASCII incompatible codecs than Asia does).

This means we've been judiciously adding surrogateescape to interfaces as
we decide the increase in convenience justifies any increased risk of
data corruption. For Python 3.5, this is `also being applied to
<http://bugs.python.org/issue19977>`__ ``sys.stdin`` and ``sys.stdout`` on
POSIX systems that claim that we should be using ``ascii`` as the default
encoding. Such a result almost certainly indicates a configuration
error in the environment, but using ascii+surrogateescape in such cases should
make for a more usable result than the current approach of ascii+strict.
There's still some risk of silent data corruption in the face of ASCII
incompatible encodings, but the assumption is that systems that are
configured with a non-ASCII compatible encoding should already have
relatively robust configurations that avoid ever relying on the default POSIX
locale.

This is an area where we're genuinely open to the case being made for
different defaults, or additional command line or environment variable
configuration options. POSIX is just seriously broken in this space, and
we're having to trade-off user convenience against the risk of silent data
corruption - that means the "right answer" is *not* obvious, and any PEP
proposing a change needs to properly account for the rationale behind the
current decision (in particular, it has to account for the technical
limitations in the startup code that create the coupling to the default
locale encoding reported by the operating system, which may require a
change on the scale of :pep:`432` to actually fix properly).


What changes in Python 3 have been made specifically to simplify migration?
---------------------------------------------------------------------------

The biggest change made specifically to ease migration from Python 2 was the
reintroduction of Unicode literals in Python 3.3 (in :pep:`414`). This
allows developers supporting both Python 2 and 3 in a single code base to
easily distinguish binary literals, text literals and native strings, as
``b"binary"`` means bytes in Python 3 and str in Python 2, ``u"text"``
means str in Python 3.3+ and unicode in Python 2, while ``"native"`` means
str in both Python 2 and 3.

The restoration of binary interpolation support in Python 3.5 was designed in
such as way as to also serve to make a lot of 8-bit string interpolation
operations in Python 2 code "just work" in Python 3.5+.

A smaller change to simplify migration was the reintroduction of the
non-text encoding codecs (like ``hex_codec``) in Python 3.2, and the
restoration of their convenience aliases (like ``hex``) in Python 3.4. The
``codecs.encode`` and ``codecs.decode`` convenience functions allow them to
be used in a single source code base (since those functions have been present
and covered by the test suite since Python 2.4, even though they were only
added to the documentation recently).

The WSGI update in :pep:`3333` also standardised the Python 3 interface
between web servers and frameworks, which is what allowed the web frameworks
to start adding Python 3 support with the release of Python 3.2.

A number of standard library APIs that were originally either binary only or
text only in Python 3 have also been updated to accept either type. In
these cases, there is typically a requirement that the "alternative" type be
strict 7-bit ASCII data - use cases that need anything more than that are
expected to do their encoding or decoding at the application boundary rather
than relying on the implicit encoding and decoding provided by the affected
APIs. This is a concession in the Python 3 text model specifically designed
to ease migration in "pure ASCII" environments - while relying on it can
reintroduce the same kind of obscure data driven failures that are seen
with the implicit encoding and decoding operations in Python 2, these APIs
are at least unlikely to silently corrupt data streams (even in the presence
of data encoded using a non-ASCII compatible encoding).


.. _other-changes:

What other changes have occurred that simplify migration?
---------------------------------------------------------

The original migration guides unconditionally recommended running an
applications test suite using the ``-3`` flag in Python 2.6 or 2.7 (to
ensure no warnings were generated), and then using the ``2to3`` utility
to perform a one-time conversion to Python 3.

That approach is still a reasonable choice for migrating a fully integrated
application that can completely abandon Python 2 support at the time of the
conversion, but is no longer considered a good option for migration of
libraries, frameworks and applications that want to add Python 3 support
without losing Python 2 support. The approach of running ``2to3``
automatically at install time is also no longer recommended, as it creates
an undesirable discrepancy between the deployed code and the code in source
control that makes it difficult to correctly interpret any reported
tracebacks.

Instead, the preferred alternative in the latter case is now to create a
single code base that can run under both Python 2 and 3. The `six`_
compatibility library can help with several aspects of that, and the
`python-modernize`_ utility is designed to take existing code that supports
older Python versions and update it to run in the large common subset of
Python 2.6+ and Python 3.3+ (or 3.2+ if the unicode literal support in
Python 3.3 isn't needed).

The "code modernisation" approach also has the advantage of being able to be
done incrementally over several releases, as failures under Python 3 can be
addressed progressively by modernising the relevant code, until eventually
the code runs correctly under both versions. Another benefit of this
incremental approach is that this modernisation activity can be undertaken
even while waiting for other dependencies to add Python 3 support.

More recently, the `python-future`_ project was created to assist those
developers that would like to primarily write Python 3 code, but would
also like to support their software on Python 2 for the benefit of
potential (or existing) users that are not themselves able to upgrade to
Python 3.

The addition of the ``pylint --py3k`` flag was designed to make it easier for
folks to ensure that code migrated to the common subset of Python 2 and Python
3 remained there rather than reintroducing Python 2 only constructs.

The `landing page for the Python documentation <http://docs.python.org>`__
was also switched some time ago to display the Python 3 documentation by
default, although deep links still refer to the Python 2 documentation in
order to preserve the accuracy of third party references (see :pep:`430`
for details).


What future changes in Python 3 are expected to further simplify migration?
---------------------------------------------------------------------------

Most of the changes designed to further simplify migration landed in Python 3.5.

One less obviously migration related aspect of those changes is that the new
gradual typing system is designed to allow Python 2 applications to be
typechecked as if they were Python 3 applications, and hence many potential
porting problems detected even if they're not covered by tests, or the test
suite can't yet be run on Python 3.


Didn't you strand the major alternative implementations on Python 2?
--------------------------------------------------------------------

Cooperation between the major implementations (primarily CPython, PyPy,
Jython, IronPython, but also a few others) has never been greater than
it has been in recent years.
The core development community that handles both the language definition
and the CPython implementation includes representatives from all of those
groups.

The language moratorium that severely limited the kinds of changes
permitted in Python 3.2 was a direct result of that collaboration - it
gave the other implementations breathing room to catch up to Python 2.7.
That moratorium was only lifted for 3.3 with the agreement of the development
leads for those other implementations.  Significantly, one of the most
disruptive aspects of the 3.x transition for CPython and PyPy (handling all
text as Unicode data) was already the case for Jython and IronPython, as
they use the string model of the underlying JVM and CLR platforms.

We have also instituted `new guidelines`_ for CPython development which
require that new standard library additions be granted special dispensation
if they are to be included as C extensions without an API compatible Python
implementation.

Python 3 specifically introduced :exc:`ResourceWarning`, which alerts
developers when they are relying on the garbage collector to clean up
external resources like sockets. This warning is off by default, but
switched on automatically by many test frameworks. The goal of this warning
is to detect any cases where ``__del__`` is being used to clean up a
resource, such as a file or socket or database connection. Such cases are
then updated to use either explicit resource management (via a
``with`` or ``try`` statement) or else switched over to :mod:`weakref` if
non-deterministic clean-up is considered appropriate (the latter is quite
rare in the standard library). The aim of this effort is specifically to
ensure that the entire standard library will run correctly on Python
implementations that don't use refcounting for object lifecycle management.

Finally, Python 3.3 converted the bulk of the import system over to pure
Python code so that all implementations can finally start sharing a common
import implementation. Some work will be needed from each implementation to
work out how to bootstrap that code into the running interpreter (this was
one of the trickiest aspects for CPython), but once that hurdle is passed
all future import changes should be supported with minimal additional effort.

All that said, there's often a stark difference in the near term *goals* of
the core development team and the developers for other implementations.
Criticism of the Python 3 project has been somewhat vocal from a number of
PyPy core developers, and that makes sense when you consider that one of
the core aims of PyPy is to provide a better runtime for *existing* Python
applications. However, despite those reservations, PyPy was still the first
of the major alternative implementations to support Python 3 (with the
initial release of their PyPy3 runtime in June 2014). The initial PyPy3
release targeted Python 3.2 compatibility, but the changes needed to catch
up on subsequent Python 3 releases are relatively minor compared to the
changes between Python 2 and Python 3, and the PyPy team received a funded
development grant from Mozilla to bring PyPy3 at least up to Python 3.5
compatibility. Work also continues on another major compatibility project
for PyPy, numpypy, which aims to integrate PyPy with the various components
of the scientific Python stack.

.. note:: The info below on Jython and IronPython is currently quite dated.
   This section should also be updated to mention the new Python 3 only
   bytecode-focused implementations targeting the JVM (BeeWare's VOC), and
   JavaScript runtimes (BeeWare's Batavia)

Jython's development efforts are currently still focused on getting their
currently-in-beta Python 2.7 support to a full release, and there is also
some significant work happening on JyNI (which, along the same lines as
PyPy's numpypy project, aims to allow the use of the scientific Python stack
from the JVM).

The IronPython folks have `started working on
<http://blog.ironpython.net/2014/03/ironpython-3-update.html>`__ a Python 3
compatible version, but there currently isn't a target date for a release.
IronClad already supports the use of `scientific libraries from IronPython
<https://www.enthought.com/repo/.iron/>`__.

One interesting point to note for Jython and IronPython is that the changes
to the Python 3 text model bring it more into line with the text models of
the JVM and the CLR. This may mean that projects updated to run in the
common subset of Python 2 and 3 will be more likely to run correctly on
Jython and IronPython, and once they implement Python 3 support, the
compatibility of Python 3 only modules should be even better.

.. _language moratorium: http://www.python.org/dev/peps/pep-3003/
.. _new guidelines: http://www.python.org/dev/peps/pep-0399/


.. _abandoning-users:

Aren't you abandoning Python 2 users?
-------------------------------------

We're well aware of this concern, and have taken what steps we can to
mitigate it.

First and foremost is the extended maintenance period for the
Python 2.7 release. We knew it would take some time before the Python 3
ecosystem caught up to the Python 2 ecosystem in terms of real world
usability. Thus, the extended maintenance period on 2.7 to ensure it
continues to build and run on new platforms. While python-dev maintenance
of 2.7 was originally slated to revert to security-fix only mode in July
2015, Guido extended that out to 2020 at PyCon 2014. We're now working
with commercial redistributors to help ensure the appropriate resources
are put in place to actually meet that commitment. In addition to the
ongoing support from the core development team, 2.6 will still be
supported by enterprise Linux vendors until at least 2020, while Python 2.7
will be supported until at least 2024.

We have also implemented various mechanisms which are designed to ease the
transition from Python 2 to Python 3. The ``-3`` command line switch in
Python 2.6 and 2.7 makes it possible to check for cases where code is going
to change behaviour in Python 3 and update it accordingly.

The automated ``2to3`` code translator can handle many of the mechanical
changes in updating a code base, and the `python-modernize`_ variant
performs a similar translation that targets the (large) common subset of
Python 2.6+ and Python 3 with the aid of the `six`_ compatibility module,
while `python-future` does something similar with its ``futurize`` utility.

:pep:`414` was implemented in Python 3.3 to restore support for explicit
Unicode literals primarily to reduce the number of purely mechanical code
changes being imposed on users that are doing the right thing in Python 2
and using Unicode for their text handling.

One outcome of some of the discussions at PyCon 2014 was the ``pylint --py3k``
utility to help make it easier for folks to migrate software incrementally and
opportunistically, first switching to the common subset running on Python 2.7,
before migrating to the common subset on Python 3.

So far we've managed to walk the line by persuading our Python 2 users that
we aren't going to leave them in the lurch when it comes to appropriate
platform support for the Python 2.7 series, thus allowing them to perform the
migration on their own schedule as their dependencies become available,
while doing what we can to ease the migration process so that following our
lead remains the path of least resistance for the future evolution of the
Python ecosystem.

:pep:`404` (yes, the choice of PEP number is deliberate - it was too good
an opportunity to pass up) was created to make it crystal clear that
python-dev has no intention of creating a 2.8 release that backports
2.x compatible features from the 3.x series. After you make it through
the opening Monty Python references, you'll find the explanation
that makes it unlikely that anyone else will take advantage of the "right
to fork" implied by Python's liberal licensing model: we had very good
reasons for going ahead with the creation of Python 3, and very good
reasons for discontinuing the Python 2 series. We didn't decide to disrupt
an entire community of developers just for the hell of it - we did it
because there was a core problem in the language design, and a backwards
compatibility break was the only way we could find to solve it once and
for all.

For the inverse question relating to the concern that the existing migration
plan is too *conservative*, see :ref:`slow-uptake`.

.. _python-modernize: https://github.com/mitsuhiko/python-modernize
.. _six: http://pypi.python.org/pypi/six
.. _python-future: http://python-future.org/index.html


What would it take to make you change your minds about the current plan?
------------------------------------------------------------------------

With both the Debian/Ubuntu and Fedora/RHEL/CentOS ecosystems well
advanced in their migration plans, public cloud providers offering Python 3
in addition to Python 2, major commercial end users like Facebook, Google and
Dropbox migrating, and the PSF's own major services like python.org and the
Python Package Index switching to Python 3, the short answer here is "That's
not going to happen".

While a crash in general Python adoption might have made us change our minds,
Python ended up working its way into more and more niches *despite* the
Python 3 transition, so the only case that could be made is "adoption would
be growing even faster without Python 3 in the picture", which is a hard
statement to prove (particularly when we suspect that at least some of
the growth in countries where English is not the primary spoken language
is likely to be *because* of Python 3 rather than in spite of it, and that
the Python 3 text model is in a much better position to serve as a bridge
between the POSIX text model and the JVM and CLR text models than the Python 2
model ever was).

Another scenario that would have made us seriously question our current
strategy is if professional educators had told us that Python 2 was a better
teaching language, but that didn't happen - they're amongst Python 3's more
vocal advocates, encouraging the rest of the community to "just upgrade
already".


Wouldn't a Python 2.8 release help ease the transition?
-------------------------------------------------------

In a word: no. In several words: maybe, but at such a high cost, the core
development team consider it a much better idea to invest that effort in
improving Python 3, migration tools and helping to port libraries and
applications (hence why credible contributors can apply to the PSF for a
grant to help port key libraries to Python 3, but PSF funding isn't available
for a Python 2.8 release).

The rationale for this proposal appears to be that if backporting Python 3
changes to Python 2.6 and 2.7 was a good idea to help Python 3 adoption,
then continuing to do so with a new Python 2.8 release would also be a
good idea.

What this misses is that those releases were made during a period when the
core development team was still in the process of ensuring that Python 3 was
in a position to stand on its own as a viable development platform. We
*didn't want* conservative users that were currently happy with Python 2
to migrate at that point, as we were still working out various details to
get it back to feature parity with Python 2. One of the most notable of
those was getting a usable WSGI specification back in 3.2, and another being
the restoration of Unicode literals in 3.3 to help with migration from Python
2.

If we hadn't considered Python 3.2 to be at least back to parity with
Python 2.7, *that* is when we would have decided to continue on to do a
Python 2.8 release. We're even less inclined to do so now that Python 3
has several additional years of feature development under its belt relative to
the Python 2 series.

There *are* parts of the Python 3 standard library that are also useful in
Python 2. In those cases, they're frequently available as backports on
the Python Package Index (including even a backport of the new asynchronous
IO infrastructure).

There are also various language level changes that are backwards compatible
with Python 2.7, and the `Tauthon project`_ was started specifically
to create a hybrid runtime implementation that expanded the "common subset"
of Python 2 & 3 to include those additional features.

However, I think a key point that is often missed in these discussions is that
the adoption cycles for new versions of the core Python runtime have *always*
been measured in years due to the impact of stable platforms like Red Hat
Enterprise Linux.

Consider the following map of RHEL/CentOS versions to Python versions
(release date given is the *Python* release date, and Python 2.5 was
skipped due to RHEL5 being published not long before it was released in
September 2006):

* 4 = 2.3 (first released July 2003)
* 5 = 2.4 (first released November 2004)
* 6 = 2.6 (first released October 2008)
* 7 = 2.7 (first released July 2010)

Now consider these Twisted compatibility requirements (going by the
modification dates on the tagged INSTALL file):

* 10.0 dropped Python 2.3 in March 2010
* 10.2 dropped Python 2.4 (Windows) in November 2010
* 12.0 dropped Python 2.4 (non-Windows) in February 2012
* 12.2 dropped Python 2.5 in August 2012
* 15.4 dropped Python 2.6 in September 2015

Python 2.6 compatibility was still required more than 7 years after its
original release, and didn't get dropped until well after the first CentOS 7
release was available (not to mention the earlier release of a Python 2.7
SCL).

I believe Twisted has one of *the* most conservative user bases in the
Python community, and I consider this one of the main reasons we see this
general pattern of only dropping support for an older release 6-7 years
after it was first made available. That's also why I considered the Twisted
developers a key audience for any increases in the scope of single source
support in Python 3.5 (and their support for the idea was certainly one of
the factors behind the planned return of binary interpolation support).

That's the way the path to Python 3 will be smoothed at this point: by
identifying blockers to migration and knocking them down, one by one. The
PSF has helped fund the migration of some key libraries. Barry Warsaw drove
a fair amount of Python 3 migration work for Ubuntu at Canonical. Victor
Stinner is working hard to encourage and support the OpenStack migration. I
have been offering advice and encouragement to Bohuslav Kabrda (the main
instigator of Fedora's migration to Python 3), Petr Viktorin, and other members
of Red Hat's Python maintenance team, as well as helping out with
Fedora policy recommendations on supporting parallel Python 2 and 3 stacks (I
have actually had very little to do with Red Hat's efforts to support Python
3 overall, as I haven't needed to. Things like Python 3 support in Red Hat
Software Collections and OpenShift Online happened because other folks at
Red Hat made sure they happened). Guido approved the restoration of Unicode
literal support after web framework developers realised they couldn't mask
that particular change for their users, and he has also approved the
restoration of binary interpolation support. I went through and made the
binary transform codecs that had been restored in Python 3.2 easier to
discover and use effectively in Python 3.4. R. David Murray put in a lot
of time and effort to actually handle Unicode sensibly in the ``email``
module, Brett Cannon has been updating the official migration guide based
on community feedback, etc, etc (I'm sure I'm missing a bunch of other
relevant changes).

Outside of CPython and its documentation, Benjamin Peterson published the
``six``, Lennart Regebro put together his excellent guide for porting,
Armin Ronacher created ``python-modernize`` and Ed Schofield created
``python-future``. Multiple folks have contributed patches to a wide
variety of projects to allow them to add Python 3 support.


Aren't you concerned Python 2 users will abandon Python over this?
------------------------------------------------------------------

Certainly - a change of this magnitude is sufficiently disruptive that
many members of the Python community are legitimately upset at the impact
it has had on them.

This is particularly the case for users that had never personally been
bitten by the broken Python 2 Unicode model, either because they work
in an environment where almost all data is encoded as ASCII text
(increasingly uncommon, but still not all that unusual in English speaking
countries) or else in an environment where the appropriate infrastructure
is in place to deal with the problem even in Python 2 (for example, web
frameworks hide most of the problems with the Python 2 approach from
their users).

Another category of users are upset that we chose to stop adding new
features to the Python 2 series, and have been `quite emphatic`_ that attempts
to backport features (other than via PyPI modules like ``unittest2``,
``contextlib2`` and ``configparser``) are unlikely to receive significant
support from python-dev.  As long as they don't attempt to present themselves
as providing official Python releases, we're not *opposed* to such efforts -
it's merely the case that (outside a few specific exceptions like :pep:`466`)
we aren't interested in doing them ourselves, and are unlikely to devote
significant amounts of time to assisting those that *are* interested.

A third category of user negatively affected by the change are those users
that deal regularly with binary data formats and had mastered the
idiosyncrasies of the Python 2 text model to the point where writing
correct code using that model was effortless. The kinds of hybrid
binary-or-text APIs that the ``str`` type made easy in Python 2 can be
relatively awkward to write and maintain in Python 3 (or in the common
subset of the two languages). While native Python 3 code can generally
simply avoid defining such APIs in the first place, developers porting
libraries and frameworks from Python 2 generally have little choice, as
they have to continue to support both styles of usage in order to allow
their *users* to effectively port to Python 3.

However, we have done everything we can to make migrating to Python 3 the
easiest exit strategy for Python 2, and provided a fairly leisurely time
frame for the user community to make the transition. Full maintenance of
Python 2.7 has now been extended to 2020, source only security releases
may continue for some time after that, and, as noted above, I expect
enterprise Linux vendors and other commercial Python redistributors to
continue to provide paid support for some time after community support ends.

Essentially, the choices we have set up for Python 2 users that find
Python 3 features that are technically backwards compatible with Python 2
attractive are:

* Live without the features for the moment and continue to use Python 2.7
* For standard library modules/features, use a backported version from PyPI
  (or create a backport if one doesn't already exist and the module doesn't
  rely specifically on Python 3 only language features)
* Migrate to Python 3 themselves
* Fork Python 2 to add the missing features for their own benefit
* Migrate to a language other than Python

The first three of those approaches are all fully supported by python-dev.
Many standard library additions in Python 3 started as modules on PyPI and
thus remain available to Python 2 users. For other cases, such as ``unittest``
or ``configparser``, the respective standard library maintainer also maintains
a PyPI backport.

The fourth choice exists as the `Tauthon project`_, so it will be interesting
to see if that gains significant traction with developers and platform
providers.

The final choice would be unfortunate, but we've done what we can to make
the other alternatives (especially the first three) more attractive.


.. _quite emphatic: http://www.python.org/dev/peps/pep-0404/


Doesn't this make Python look like an immature and unstable platform?
---------------------------------------------------------------------

Again, many of us in core development are aware of this concern, and
have been taking active steps to ensure that even the most risk averse
enterprise users can feel comfortable in adopting Python for their
development stack, despite the current transition.

Obviously, much of the content in the answers above regarding the
viability of Python 2 as a development platform, with a clear future
migration path to Python 3, is aimed at enterprise users. Government agencies
and large companies are the environments where risk management tends to come
to the fore, as the organisation has something to lose. The start up and
open source folks are far more likely to complain that the pace of Python
core development is *too slow*.

The main change to improve the perceived stability of Python 3 is that
we've started making greater use of the idea of "documented
deprecation". This is exactly what it says: a pointer in the documentation
to say that a particular interface has been replaced by an alternative we
consider superior that should be used in preference for new code. We
have no plans to remove any of these APIs from Python - they work, there's
nothing fundamentally wrong with them, there is just an updated alternative
that was deemed appropriate for inclusion in the standard library.

Programmatic deprecation is now reserved for cases where an API or feature
is considered so fundamentally flawed that using it is very likely to cause
bugs in user code. An example of this is the deeply flawed
``contextlib.nested`` API which encouraged a programming style that would
fail to correctly close resources on failure. For Python 3.3, it was finally
replaced with a superior incremental ``contextlib.ExitStack`` API which
supports similar functionality without being anywhere near as error prone.

Secondly, code level deprecation warnings are now silenced by default. The
expectation is that test frameworks and test suites will enable them (so
developers can fix them), while they won't be readily visible to end users
of applications that happen to be written in Python. (This change can
actually cause problems with ad hoc user scripts breaking when upgrading to
a newer version of Python, but the longevity of Python 2.7 actually works in
our favour on that front)

Finally, and somewhat paradoxically, the introduction of `provisional APIs`
in Python 3 is a feature largely for the benefit of enterprise users. This
is a documentation marker that allows us to flag particular APIs as
potentially unstable. It grants us a full release cycle (or more) to ensure
that an API design doesn't contain any nasty usability traps before
declaring it ready for use in environments that require rock solid
backwards compatibility guarantees.

.. _provisional APIs: http://www.python.org/dev/peps/pep-0411/


Why wasn't **I** consulted?
---------------------------

Technically, even the core developers weren't consulted: Python 3 happened
because the creator of the language, Guido van Rossum, wanted it
to happen, and Google paid for him to devote half of his working hours to
leading the development effort.

In practice, Guido consults extensively with the other core developers, and
if he can't persuade even us that something is a good idea, he's likely to
back down. In the case of Python 3, though, it is our collective opinion
that the problems with Unicode in Python 2 are substantial enough to
justify a backwards compatibility break in order to address them, and
that continuing to maintain both versions in parallel indefinitely would
not be a good use of limited development resources.

We as a group also continue to consult extensively with the authors of other
Python implementations, authors of key third party frameworks, libraries and
applications, our own colleagues and other associates, employees of key
vendors, Python trainers, attendees at Python conferences, and, well, just
about anyone that cares enough to sign up to the python-dev or python-ideas
mailing lists or add their Python-related blog to the Planet Python feed,
or simply discuss Python on the internet such that the feedback
eventually makes it way back to a place where we see it.

Some notable changes within the Python 3 series, specifically :pep:`3333`
(which updated the Web Server Gateway Interface to cope with the Python 3
text model) and :pep:`414` (which restored support for explicit Unicode
literals) have been driven primarily by the expressed needs of the web
development community in order to make Python 3 better meet their needs.

The restoration of binary interpolation support in Python 3.5 is similarly
intended to increase the size of the common subset of Python 2 and Python 3
in a way that makes it easier for developers to migrate to the new version
of the language (as well as being a useful new feature for Python 3 in its
own right).

If you want to keep track of Python's development and get some idea of
what's coming down the pipe in the future, it's all
`available on the internet`_.

.. _available on the internet: http://docs.python.org/devguide/communication.html

But <name> says Python 3 was a waste of time/didn't help/made things worse!
---------------------------------------------------------------------------

One previously popular approach to saying why Python 2 should be used over
Python 3 even for *new* projects was to appeal to the authority of someone like
Armin Ronacher (creator of Jinja2, Flask, Click, etc) or Greg Wilson (creator
of Software Carpentry).

The piece missing from that puzzle is the fact that Guido van Rossum, the
creator of Python, *and* every core developer of CPython, have not only been
persuaded that the disruption posed by the Python 3 transition is worth the
effort, but have been busily adding the features we notice missing from both
Python 2 and 3 solely to the Python 3 series since the feature freeze for
Python 2.7 back in 2010.

Where's the disconnect? Well, it arises in a couple of ways. Firstly, when
creating Python 3, we *deliberately made it worse than Python 2* in
particular areas. That sounds like a ridiculous thing for a language design
team to do, but programming language design is a matter of making trade-offs
and if you try to optimise for everything at once, you'll end up with an
unreadable mess that isn't optimised for anything. In many of those cases,
we were trading problems we considered unfixable for ones that could at least
be solved in theory, even if they haven't been solved *yet*.

In Armin's case, the disconnect was that his primary interest is in writing
server components for POSIX systems, and cross-platform command clients for
those applications. This runs into issues, because Python 3's operating
system integration could get confused in a few situations:

* on POSIX systems (other than Mac OS X), in the default C locale
* on POSIX systems (other than Mac OS X), when ssh environment forwarding
  configures a server session with the client locale and the client and
  server have differing locale settings
* at the Windows command line

This change is due to the fact that where Python 2 decodes from 8-bit data
to Unicode text *lazily* at operating system boundaries, Python 3 does so
*eagerly*. This change was made to better accommodate Windows systems (where
the 8-bit APIs use the mbcs codec, rendering them effectively useless), but
came at the cost of being more reliant on receiving correct encoding and
decoding advice from the operating system. Operating systems are normally
pretty good about providing that info, but they fail hard in the above
scenarios.

In almost purely English environments, none of this causes any problems, just
as the Unicode handling defects in Python 2 tend not to cause problems in
such environments. In the presence of non-English text however, we had to
decide between cross-platform consistency (i.e. assuming UTF-8 everywhere),
and attempting to integrate correctly with the encoding assumptions of other
applications on the same system. We opted for the latter approach, primarily
due to the dominance of ASCII incompatible encodings in East Asian countries
(ShiftJIS, ISO-2022, GB-18030, various CJK codecs, etc). For ordinary user space
applications, including the IPython Notebook, this already works fine. For other
code, we're now working through the process of assuming UTF-8 as the default
binary encoding when the operating system presents us with dubious encoding
recommendations (that will be a far more viable assumption in 2016 than it was
in 2008).

For anyone that would like to use Python 3, but is concerned by Armin
Ronacher's comments, the best advice I can offer is to *use his libraries*
to avoid those problems. Seriously, the guy's brilliant - you're unlikely to
go seriously wrong in deciding to use his stuff when it applies to your
problems. It offers a fine developer experience, regardless of which version
of Python you're using. His complaints are about the fact that *writing those
libraries* became more difficult in Python 3 in some respects, but he gained
the insight needed to comprehensively document those concerns the hard way:
by porting his code. His feedback on the topic was cogent and constructive
enough that it was cited as one of the reasons he received a Python Software
Foundation Community Service Award in
`October 2014 <https://www.python.org/community/awards/psf-awards/#october-2014>`__.

The complaints from the Software Carpentry folks (specifically Greg Wilson)
were different. Those were more about the fact that we hadn't done a very
good job of explaining the problems that the Python 3 transition was
designed to fix. This is an example of something Greg himself calls "the
curse of knowledge": experts don't necessarily know what other people
*don't know*. In our case, we thought we were fixing bugs that tripped
up everyone. In reality, what we were doing was fixing things that *we*
thought were still too hard, even with years (or decades in some cases) of
Python experience. We'd waste memory creating lists that we then just
iterated over and threw away, we'd get our Unicode handling wrong so our
applications broke on Windows narrow builds (or just plain broke the first
time they encountered a non-ASCII character or text in multiple encodings),
we'd lose rare exception details because we had a latent defect in an
error handler. We baked fixes for all of those problems (and more) *directly
into the design* of Python 3, and then became confused when other Python
users tried to tell us Python 2 wasn't broken and they didn't see what
Python 3 had to offer them. So we're now in a position where we're having to
unpack years (or decades) of experience with Python 2 to explain why we
decided to put that into long term maintenance mode and switch our feature
development efforts to Python 3 instead.

After hearing Greg speak on this, I'm actually really excited when I hear
Greg say that Python 3 is no harder to learn than Python 2 for English
speakers, as we took some of the more advanced concepts from Python 2 and
made them *no longer optional* when designing Python 3. The Python 3
"Hello World!" now introduces users to string literals, builtins, function
calls and expression statements, rather than just to string literals and a
single dedicated print statement. Iterators arrive much earlier in the
curriculum than they used to, as does Unicode. The chained exceptions that
are essential for improving the experience of debugging obscure production
failures can present some readability challenges for new users. If we've
managed to front load all of that hard earned experience into the base
design of the language and the end result is "just as easy to learn as
Python 2", then I'm *happy* with that. It means we were wrong when we thought
we were making those changes for the benefit of beginners - it turns out
English speaking beginners aren't at a point where the issues we addressed
are even on their radar as possible problems. But Greg's feedback now
suggests to me that we have actually succeeded in removing some of
the barriers between competence and mastery, without *harming* the beginner
experience. There are also other changes in Python 3, like the removal of
the "__init__.py" requirement for package directories, the improvements to
error messages when functions are called incorrectly, the inclusion of
additional standard library modules like statistics, asyncio and ipaddress,
the bundling of pip, and more automated configuration of Windows systems in
the installer that should genuinely improve the learning experience for new
users.

Greg's also correct that any *renaming* of existing standard library
functionality should be driven by objective user studies - we learned that
the hard way by discovering that the name changes and rearrangements we did
in the Python 3 transition based on our own intuition were largely an
annoying waste of time that modules like ``six`` and ``future`` now have to
help folks moving from Python 2 to Python 3 handle. However, we're not
exactly drowned in offers to do that research, so unless someone can figure
out how to get it funded and executed, it isn't going to happen any time
soon. As soon as someone does figure that out, though, I look forward to
seeing Python Enhancement Proposals backed specifically by research done to
make the case for particular name changes, including assessments of the
additional cognitive load imposed by students having to learn both the new
names suggested by the usability research and the old names that will still
have to be kept around for backwards compatibility reasons. In the meantime,
we'll continue with the much lower cost "use expert intuition and arguing on
the internet to name new things, leave the names of existing things alone"
approach. That low cost option almost certainly doesn't find *optimal*
names for features, but it does tend to find names that are *good enough*.

The other piece that we're really missing is feedback from folks teaching
Python to users in languages *other than English*. Much of the design of
Python 3 is aimed at working better with East Asian and African languages
where there are no suitable 8-bit encodings - you really need the full power
of Unicode to handle them correctly. With suitable library support, Python 2
can be made to handle those languages at the application level, but
Python 3 aims to handle them at the language and interpreter level - Python
shouldn't fail just because a user is attempting to run it from their home
directory and their name can't be represented using the latin-1 alphabet
(or koi8-r, or some other 8-bit encoding). Similarly, naming a module in
your native language shouldn't mean that Python can't import it, but in
Python 2, module names (like all identifiers) are limited to the ASCII
character set. Python 3 lifts the limitations on non-ASCII module names
and identifiers in general, meaning that imposing such restrictions enters
the domain of project-specific conventions that can be enforced with tools
like pylint, rather than being an inherent limitation of the language itself.


But, but, surely fixing the GIL is more important than fixing Unicode...
------------------------------------------------------------------------

With Eric Snow's publication of his intent to investigate enhancing
CPython's existing subinterpreter model to provide native support for
Communicating Sequential Processes based parallel execution, the discussion of
Python's multicore processing support that previously appeared here has been
moved out to its own :ref:`article <multicore-python>`.


Well, why not just add JIT compilation, then?
---------------------------------------------

.. note:: This answer was written for Python 3.5. While CPython 3.6 still
   doesn't ship with a JIT compiler by default, it *does* ship with a dynamic
   `frame evaluation hook <https://docs.python.org/3/whatsnew/3.6.html#pep-523-adding-a-frame-evaluation-api-to-cpython>`__
   that allows third party method JITs like Pyjion to be enabled at runtime.

This is another one of those changes which is significantly easier said
than done - the problem is with the "just", not the "add JIT compilation".
Armin Rigo (one of the smartest people I've had the pleasure of meeting)
tried to provide one as an extension module (the ``psyco`` project) but
eventually grew frustrated with working within CPython's limitations and
even the limitations of existing compiler technology, so he went off and
invented an entirely new way of building language interpreters instead -
that's what the ``PyPy`` project is, a way of writing language interpreters
that also gives you a tracing JIT compiler, almost for free.

However, while PyPy is an amazing platform for running Python *applications*,
the extension module compatibility problems introduced by using a different
reference counting mechanism mean it isn't yet quite as good as CPython as
an *orchestration* system, so those users in situations where their Python
code isn't the performance bottleneck stick with the simpler platform. That
currently includes scientists, Linux vendors, Apple, cloud providers and so
on and so forth. As noted above when discussing the possible future of
concurrency in Python, it seems entirely plausible to me that PyPy will
eventually become the default *application* runtime for Python software,
with CPython being used primarily as a tool for handling orchestration tasks
and embedding in other applications, and only being used to run full
applications if PyPy isn't available for some reason. That's going to take
a while though, as vendors are currently still wary of offering commercial
support for PyPy, not through lack of technical merit, but simply because
it represents an entirely new way of creating software and they're not sure
if they trust it yet (they'll likely get over those reservations eventually,
but it's going to take time - as the CPython core development team have
good reason to know, adoption of new platforms is a slow, complex business,
especially when many users of the existing platform don't experience the
problem that the alternative version is aiming to solve).

While PyPy is a successful example of creating a *new* Python implementation
with JIT compilation support (Jython and IronPython benefit from the JIT
compilation support in the JVM and CLR respectively), the Unladen Swallow
project came about when some engineers at Google made a second attempt at
adding a JIT compiler directly to the CPython code base.

The Unladen Swallow team did have a couple of successes: they made several
improvements to LLVM to make it more usable as a JIT compiler, and they put
together an excellent set of Python macro benchmarks that are used by both
PyPy and CPython for relative performance comparisons to this day. However,
even though Guido gave in principle approval for the idea, one thing they
*didn't* succeed at doing is adding implicit JIT compilation support
directly to CPython.

The most recent attempt at adding JIT compilation to CPython is a project
called `Numba`_, and similar to ``psyco``, Numba doesn't attempt to provide
*implicit* JIT compilation of arbitrary Python code. Instead, you have to
decorate the methods you would like accelerated. The advantage of this is
that it means that Numba *doesn't* need to cope with the full dynamism of
Python the way PyPy does - instead, it can tweak the semantics within the
decorated functions to reduce the dynamic nature of the language a bit,
allowing for simpler optimisation.

.. _Numba: http://numba.pydata.org/


Anyone that is genuinely interested in getting implicit JIT support into the
default CPython implementation would do well to look into resurrecting the
`speed.python.org <http://speed.python.org/>`__ project. Modelled after
the `speed.pypy.org <http://speed.pypy.org/>`__ project (and using the same
software), this project has foundered for lack of interested volunteers and
leadership. It comes back to the problem noted above - if you're using Python
for orchestration, the Python code becoming a bottleneck is usually taken as
indicating an architectural issue rather than the Python runtime being too
slow.

The availability of PyPy limits the appeal of working on adding JIT
compilation to CPython as a volunteer or sponsoring it as a commercial user
even further - if all of the extensions an application needs are also
available on PyPy, then it's possible to just use that instead, and if
they *aren't* available, then porting them or creating alternatives with
`cffi` or a pure Python implementation is likely to be seen as a more
interesting and cost effective solution than attempting to add JIT
compilation support to CPython.

I actually find it quite interesting - the same psychological and commercial
factors that work against creating Python 2.8 and towards increasing
adoption of Python 3 also work *against* adding JIT compilation support
to CPython and towards increasing adoption of PyPy for application style
workloads.


What about <insert other shiny new feature here>?
-------------------------------------------------

The suggestions that adding a new carrot like free threading or a JIT
compiler to Python 3 would suddenly encourage users that are happy with
Python 2 to migrate generally misunderstand the perspective of conservative
users.

Early adopters are readily attracted by shiny new features - that's what
makes them early adopters. And we're very grateful to the early adopters of
Python 3 - without their interest and feedback, there's no way the new
version of the language would have matured as it has over the last several
years.

However, the kinds of things that attract conservative users are very
different - they're not as attracted by shiny new features as they are by
reliability and support. For these users, the question isn't necessarily
"Why would I start using Python 3?", it is more likely to be
"Why would I stop using Python 2?".

The efforts of the first several years of Python 3 deployment were about
positioning it to start crossing that gap between early adopters and more
conservative users. Around 2014, those pieces started falling into place,
especially as more enterprise Linux vendors brought supported Python 3
offerings to market.

This means that while conservative users that are *already* using Python are
likely to stick with Python 2 for the time being ("if it isn't broken for us,
why change it?"), *new* conservative users will see a fully supported
environment, and 3 is a higher number than 2, even if the ecosystem still has
quite a bit of catching up to do (conservative users aren't going to be
downloading much directly from PyPI either - they often prefer to outsource
that kind of filtering to software vendors rather than doing it themselves).
