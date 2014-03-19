Python 3 Q & A
==============

:Published:    29th June, 2012
:Last Updated: 15th March, 2014

With the long transition to "Python 3 by default" still in progress, the
question is occasionally raised as to whether or not the core Python
developers are acting as reasonable stewards of the Python language. It's
an entirely appropriate question, as Python 3 introduces backwards
incompatible changes that more obviously benefit future users of
the language than they do current users, so existing users (especially
library and framework developers) are being asked to devote time and effort
to a transition that may not benefit them directly for years to come.

Since I've seen variants of these questions several times over the years,
I now keep this as an intermittently updated record of my thoughts on the
topic (updates are generally prompted by new iterations of the questions).
You can see the full history of changes in the `source repo`_.

The views expressed below are my own. While many of them are shared by
other core developers, and I use "we" in several places where I believe
that to be the case, I don't claim to be writing on the behalf of every
core developer on every point. Several core developers (including Guido)
*have* reviewed and offered comments on this document at various points in
time, and aside from Guido noting that I was incorrect about his initial
motivation in creating Python 3, none of them has raised any objections
to specific points or the document in general.

I am also not writing on behalf of the Python Software Foundation (of which
I am a nominated member) nor on behalf of Red Hat (my current employer).
However, I do use several Red Hat specific examples when discussing
enterprise perception and adoption of the Python platform - effectively
bridging that gap between early adopters and the vast majority of prospective
platform users is kinda what Red Hat specialises in, so I consider them an
important measure of the inroads Python 3 is making into more conservative
development communities.

.. note::

   If anyone is interested in writing about these issues in more formal
   media, please get in touch to check if particular answers are still up
   to date. As noted above this article is only *intermittently* updated,
   so some of the more time-specific references may need updating.
   Alternatively, just note that the answers below reflect snapshots as of
   the "Last Updated" date given above.

As with all essays on these pages, feedback is welcome via the
`issue tracker`_ or `Twitter`_.

.. _issue tracker: https://bitbucket.org/ncoghlan/misc/issues
.. _Twitter: https://twitter.com/ncoghlan_dev


TL;DR Version
-------------

* Yes, we know this migration is disruptive.
* Yes, we know that some sections of the community have never personally
  experienced the problems with the Python 2 Unicode model that this
  migration is designed to eliminate, or otherwise prefer the closer
  alignment between the Python 2 text model and the POSIX test model.
* Yes, we know that many of those problems had already been solved by
  some sections of the community to their own satisfaction.
* Yes, we know that by attempting to fix these problems in the core Unicode
  model we have broken many of the workarounds that had been put in place
  to deal with the limitations of the old model
* Yes, we are trying to ensure there is a smooth migration path from Python
  2 to Python 3 to minimise the inevitable disruption
* Yes, we know some members of the community would like the migration to
  move faster and find the "gently, gently, there's no rush" approach of the
  core development team frustrating
* No, we did not do this lightly
* No, we do not see any other way to ensure Python remains a viable
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
it is clear that we consider that creating and promoting Python 3 is an
*easier* and *more pleasant* alternative to attempting to fix those issues
while abiding by Python 2's backwards compatibility requirements).

The revised text model in Python 3 also means that the *primary* string
type is now fully Unicode capable. This brings Python closer to the model
used in the JVM, .NET CLR and other Unicode capable Windows APIs. One
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
text (such as identifiers) now permit a much wider range of Unicode
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

This change is the key source of friction when it comes to Python 3 between
the Python core developers and other experts that have fully mastered the
Python 2 Unicode system. I've said `for
<https://mail.python.org/pipermail/python-dev/2010-June/101134.html>`__
`some
<https://mail.python.org/pipermail/python-ideas/2011-May/010381.html>`__
`time
<https://mail.python.org/pipermail/python-ideas/2011-December/012993.html>`__
that Python 3 *might* need a new third party type to better handle some of
the use cases that could be handled by the Python 2 ``str`` type, but have
been deemed out of scope for the Python 3 ``bytes`` type. Unfortunately, it
has proven `close to impossible
<https://mail.python.org/pipermail/python-ideas/2011-May/010389.html>`__
to get people to start thinking in terms of a *new
extension type* (preferably one starting life outside the standard library)
rather than repeating the mantra "please make the Python 3 ``bytes`` type a
hybrid type like the Python 2 ``str`` type". It's not always stated
explicitly, but that's generally the underlying theme of pieces like
`this one from Armin Ronacher
<http://lucumr.pocoo.org/2014/1/5/unicode-in-2-and-3/>`__ lamenting the
lost type from the Python 2 model. While Armin is entirely correct that
the removed type made that kind of hybrid API easier to write, it did so
at the cost of making it significantly harder to use the Python 2 text model
to learn how Unicode worked, as well as making it significantly harder to
avoid introducing inadvertent assumptions of ASCII compatibility in code
that should be able to handle arbitrary binary data. One of the key Python
3 design decisions was the one where Guido decided that wasn't a good
trade-off to make in the core language design, so Python 3 brings the text
model more into line with the designs used in languages like Java and C#.

This usually isn't a major problem for *new* Python 3 code - such code is
typically designed to operate in the binary domain (perhaps relying on the
methods for working with ASCII compatible segments), the text domain, or to
handle a transition between them. However, code being ported from Python 3
may need to continue to implement hybrid APIs in order to accommodate users
that make different decisions regarding whether to operate in the binary
domain or the text domain in Python 3 - because Python 2 blurred the
distinction, different users will make different choices, and forward party
libraries and frameworks may need to account for that rather than forcing
a particular answer for all users.

Accordingly, making bytes such a hybrid type is simply *not* going to happen,
as it would involve reverting to the Python 2 text model that favoured
boundary code over normal application code. However, having such a hybrid
type *available* as a power tool that boundary code developers can reach
for when they need it isn't an obviously unreasonable idea (although
actually *implementing* that type may turn out to instead provide a
clear demonstration for why we moved away from that approach when
designing the Python 3 text model).

While converting the standard library code, we haven't encountered any
situations where creating such a hybrid type seemed easier than just making
the previously implicit encoding and decoding operations explicit (especially
since we *really* don't want beginners to reach for such a type - it's at
most an advanced tool for developers of boundary code, which is the kind of
problem that beginners should be using pre-existing libraries to handle), but
it's certainly an approach worth exploring. At linux.conf.au 2014 (with some
nudging from Russell Keith-Magee of the Django project) I found a volunteer
willing to put in some time to actually experimenting with the idea, so
anyone else interested in the concept may want to take a look at Benno
Rice's (highly experimental, not actually working yet)
`prototype <https://github.com/jeamland/asciicompat>`__.

After making the initial switch in Python 3.0, we *have* made lots of
changes to improve the interoperability of the new text model with POSIX
systems and to make the new bytes type easier to work with. We've also
updated many APIs that could be used as binary or text APIs in Python 2 to
also be usable as binary or text APIs in Python 3. The only thing we flatly
refuse to do is to make changes to the core ``bytes`` type that we believe
take it back towards being usable as a hybrid binary/text type, rather than
just providing some optional facilities that make it easier to work with
ASCII compatible segments in binary data formats. I generally interpret
such proposals as indicating a fundamental misunderstanding of the
nature of the changes made to the text model in moving from Python 2 to
Python 3 (which is fair enough really, since the understanding of the full
implications of those changes evolved over a period of years on the core
development lists - I believe this answer is the first attempt at summarising
the core design ethos behind them for the benefit of those that haven't been
paying close attention to the Python 3 development process).


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
   comprehensive timeline, feel free to use this answer as a starting point.
   At least the following events should be included in a more complete list:

   * NumpPy 1.5.0 and SciPy 0.9.0 (these added Python 3 support)
   * matplotlib Python 3 support
   * IPython Python 3 support
   * Cython Python 3 support
   * SWIG Python 3 support
   * inclusion of Python 3 stacks in Linux distributions
   * links for the availability of commercially supported Python 3 stacks
     (Canonical and Red Hat are already listed, need to add ActiveState &
     Continuum Analytics. I've also been told SLES 12 will likely include
     a supported release of Python 3, but that doesn't have an official
     release date yet)
   * links for the Ubuntu and Fedora "Python 3 as default" migration plans
     (openSUSE doesn't appear to have a clear migration plan that I can find)
   * SQL Alchemy Python 3 support
   * pytz Python 3 support
   * PyOpenSSL support
   * mod_wsgi Python 3 support (first 3.x WSGI implementation)
   * Tornado Python 3 support (first 3.x async web server)
   * Pyramid Python 3 support (first major 3.x compatible web framework)
   * Django 1.5 and 1.6 (experimental and stable Python 3 support)
   * Werkzeug and Flask Python 3 support
   * requests Python 3 support
   * pyside Python 3 support (first Python 3.x Qt bindings)
   * pygtk and/or pygobject Python support
   * wxPython phoenix project
   * cx-Freeze Python 3 support
   * setuptools and pip Python 3 support
   * Pillow (PIL fork) Python 3 support
   * greenlet Python 3 support
   * pylint Python 3 support
   * Editor/IDE support for Python 3 in: PyDev,
     Python Tools for Visual Studio, PyCharm, WingIDE, Komodo (others?)
   * Embedded Python 3 support in: Blender, Kate, vim, gdb, gcc, LibreOffice
     (others?)
   * heck, the day any bar on https://python3wos.appspot.com/ or
     wedge on http://py3readiness.org/ turns green is potentially
     a significant step for some subsection of the community :)


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

**August 2007**: The first alpha release of Python 3.0 was published.

**February 2008**: The first alpha release of Python 2.6 was published
alongside the third alpha of Python 3.0. The release schedules for both
Python 2.6 and 3.0 are covered in :pep:`361`.

**October 2008**: Python 2.6 was published, including the backwards
compatible features defined for Python 3.0, along with a number of
``__future__`` imports and the ``-3`` switch to help make it practical
to add Python 3 support to existing Python 2 software (or to migrate
entirely from Python 2 to Python 3). (Python 2.6 received its final
security update in October 2013, however, support remains available
through commercial redistributors)

**December 2008**: In a fit of misguided optimism, Python 3.0 was published
with an unusably slow pure Python IO implementation - it worked tolerably
well for small data sets, but was entirely impractical for handling
realistic workloads on the CPython reference interpreter. (Python 3.0
received a single maintenance release, but was otherwise entirely
superceded by the release of Python 3.1)

**March 2009**: The first alpha release of Python 3.1, with an updated
C accelerated IO stack, was published. :pep:`375` covers the details of the
Python 3.1 release cycle.

**June 2009**: Python 3.1 final was published, providing the first version
of the Python 3 runtime that was genuinely usable for realistic workloads.
Python 3.1 is currently still receiving security updates, and will continue
to do so until June 2014.

**October 2009**: :pep:`3003` was published, declaring a moraratorium on
language level changes in Python 2.7 and Python 3.2. This was done to
deliberately slow down the pace of core development for a couple of years,
with additional effort focused on standard library improvements (as well
as some improvements to the builtin types).

**December 2009**: The first alpha of Python 2.7 was published. :pep:`373`
covers the details of the Python 2.7 release cycle.

**July 2010**: Python 2.7 final was published, providing many of the
backwards compatible features added in the Python 3.1 and 3.2 releases.
Python 2.7 is currently still fully supported by the core development team
and will continue receiving maintenance releases until at least July 2015,
and security updates for a not yet specified period beyond that.

Once the Python 2.7 maintenance branch was created, the py3k development
branch was retired: for the first time, the default branch in the main
CPython repo was the upcoming version or Python 3.

**August 2010**: The first alpha of Python 3.2 was published. :pep:`392`
covers the details of the Python 3.2 release cycle. Python 3.2 restored
preliminary support for the binary and text transform codecs that had
been removed in Python 3.0.

**October 2010**: :pep:`3333` was published to define WSGI 1.1, a Python 3
compatible version of the Python Web Server Gateway Interface.

**February 2011**: Python 3.2 final was published, providing the first
version of Python 3 with support for the Web Server Gateway Interface.
Python 3.2 is currently still receiving security updates, and an end date
for further updates has not yet been set.

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
published to make it crystal clear that the core development has no plans
to make a third parallel release in the Python 2.x series.

**March 2012**: The first alpha of Python 3.3 was published. :pep:`398`
covers the details of the Python 3.3 release cycle. Notably, Python
3.3 restored support for Python 2 style Unicode literals after Armin
Ronacher and other web framework developers pointed out that this was one
change that the web frameworks couldn't handle on behalf of their users.
:pep:`414` covers the detailed rationale for that change.

**April 2012**: Canonical publishes Ubuntu 12.04 LTS, including commercial
support for both Python 2.7 and Python 3.2.

**September 2012**: Six and half years after the inauguration of the Python
3000 project, Python 3.3 final was published as the first Python
3 release without a corresponding Python 2 feature release.

**October 2012**: :pep:`430` was published, and the `online Python
documentation <http://docs.python.org>`__ updated to present the Python 3
documentation by default. In order to preserve existing links, deep links
continue to be interpreted as referring to the Python 2.7 documentation.

**March 2013**: :pep:`434` redefined IDLE as an application shipped with
Python rather than part of the standard library, allowing the addition of
new features in maintenance releases. Significantly, this allows the
Python 2.7 IDLE to be brought more into line with the features of the Python
3.x version.

**September 2013**: Red Hat published "Red Hat Software Collections 1.0",
providing commercial support for both Python 2.7 and Python 3.3 on Red
Hat Enterprise Linux systems.

**August 2013**: The first alpha of Python 3.4 was published. :pep:`429`
covers the details of the Python 3.4 release cycle. Amongst other changes,
Python 3.4 restored full support for the binary and text transform codecs
that were reinstated in Python 3.2, while maintaining the "text encodings
only" restriction for the convenience methods on the builtin types.

**December 2013**: Red Hat published the public beta of Red Hat Enterprise
Linux 7, with Python 2.7 as the system Python. This is likely to ensure
that Python 2.7 remains a commercially supported platform until *at least*
2024.

**March 2014**: Python 3.4 final was published as the second Python 3
release without a corresponding Python 2 release. It includes several
features designed to provide a better starting experience for newcomers
to Python, such as bundling the "pip" installer by default, and including
a rich asynchronous IO library.

**April 2014**: Ubuntu 14.04 LTS, target release for the "Python 3 by
default" Ubuntu migration plan.

**June 2014**: 5 years after the first production capable Python 3.x
release

**December 2014**: Fedora 22, target release for the "Python 3 by default"
Fedora migration plan.

**Before July 2015 (tentative)**: This is still subject to discussion
amongst the core development team, but we're currently considering a
development cycle for 3.5 that is slightly shorter than usual (12-17
months rather than 18-24) in order to get some additional features that
further lower the barrier to migration from Python 2 incorporated prior
to the final full maintenance release of Python 2.7.

**July 2015**: Anticipated date for Python 2.7 to switch to security
fix only mode, ending roughly eight years of parallel maintenance of
Python 2 and 3 by the core development team for the reference interpreter.


When can we expect Python 3 to be the obvious choice for new projects?
----------------------------------------------------------------------

Going in to this transition process, my personal estimate was that
it would take roughly 5 years to get from the first production ready release
of Python 3 to the point where its ecosystem would be sufficiently mature for
it to be recommended unreservedly for all *new* Python projects.

Since 3.0 turned out to be a false start due to its IO stack being unusably
slow, I start that counter from the release of 3.1: June 27, 2009.
In the latest update of this Q&A (March 19, 2014), that puts us only
3 months away from that original goal.

In the past few years, key parts of the ecosystem have successfully added
Python 3 support. NumPy and the rest of the scientific Python stack supports
both versions, as do several GUI frameworks (including PyGame). The Pyramid,
Django and Flask web frameworks support both versions, as does the mod_wsgi
Python application server, and the py2app and cx-Freeze binary creators. The
upgrade of Pillow from a repackaging project to a full development fork also
brought PIL support to Python 3.

nltk doesn't support Python 3 in an official release yet, but an alpha
release with Python 3 compatibility is available.

For AWS users, the main ``boto`` library is Python 2 only, so Python 3
users will either need to try to Python 3 branch in the main boto repo
(which appears to be quite old at this point), or else try `boto3
<http://boto3.readthedocs.org>`__ that is intended to be an eventual
replacement for the original ``boto``.

This means that Twisted and gevent are the main critical dependencies that
don't support Python 3 yet, but solid progress has been made in both cases.
In the case of gevent, gevent 1.1 is likely to feature Python 3 compatibility
(there has been a working fork with Python 3 support for several months).
Python 3 support in Twisted may take a while longer to arrive, but *new*
projects have the option of using Guido van Rossum's ``asyncio`` module
instead (this is a new addition to the standard library in Python 3.4, also
`available on PyPI <https://pypi.python.org/pypi/asyncio>`__ for Python 3.3).
Victor Stinner has backported ``asyncio`` to Python 2 as the `Trollius
<https://pypi.python.org/pypi/trollius>`__, allowing it to be used in
single source Python 2/3 code bases. The `Tornado web server
<http://www.tornadoweb.org/en/stable/>`__ is another option for
asynchronous IO support that already runs on both Python 2 and Python 3.

If there is any functionality that py2exe provides that is not available
in cx-Freeze, then that may also cause problems for affected projects.

There is a `Python 2 or Python 3`_ page on the Python wiki which aims to
provides a reasonably up to date overview of the current state of the
transition.

I think Python 3.4 is a superior language to 2.7 in almost every way (with
the error reporting improvements being the ones I miss most in my day job
working on a Python 2.6 application). There are a few concepts like
functions, iterables and Unicode that need to be introduced earlier than
was needed in Python 2, and there are still a couple of rough edges in
adapting between the POSIX text model and the Python 3 one (in particular,
support for direct interpolation into binary data formats that contain ASCII
compatible text segments is now expected to return in Python 3.5).

Python 3.4 takes a big step forward in usability for beginners by providing
``pip`` by default, as well as updating the native virtual environment tool
(``pyvenv``) to automatically install pip into new environments. While
trainers in enterprise environments may still wish to teach Python 2 by
default for a few more years, this particular change creates a strong
incentive for community workshops to favour Python 3.4+ after it is
released early in 2014. Note that it is still entirely reasonable to learn
Python 2 after learning Python 3 - the intent at this stage of the transition
is to encourage new users to learn Python 3 *first*, and then take advantage
of the backports and other support modules on PyPI to bring their Python 2.x
usage as close to writing Python 3 code as is practical.

Support in enterprise Linux distributions is also a key point for uptake
of Python 3. Canonical have already shipped a supported version (Python 3.2
in Ubuntu 12.04 LTS) with a `stated goal`_ of eliminating Python 2 from the
live install CD for 14.04 LTS. A Python 3 stack has existed in Fedora since
Fedora 13 and has been growing over time, and there is now a stated goal
to remove Python 2 from the live install CDs by the `end of 2014`_
(Fedora 22). Red Hat also now ship a fully supported Python 3.3 runtime as
part of our `Red Hat Software Collections`_ product and the OpenShift
Enterprise self-hosted Platform-as-a-Service offering (and I assume we'll
see 3.4 added to that mix some time in 2014).

The Arch Linux team have gone even further, making Python 3 the
`default Python`_ on Arch installations. I am `dubious`_ as to the wisdom
of that strategy at this stage of the transition, but I certainly can't
complain about the vote of confidence!

The OpenStack project, likely the largest open source Python project, is
also in the process of migrating from Python 2 to Python 3, and maintains
a detailed `status tracking <https://wiki.openstack.org/wiki/Python3>`__
page for the migration.

.. _Python 2 or Python 3: http://wiki.python.org/moin/Python2orPython3
.. _stated goal: https://wiki.ubuntu.com/Python
.. _end of 2014: https://fedoraproject.org/wiki/Changes/Python_3_as_Default
.. _Red Hat Software Collections: http://developerblog.redhat.com/2013/09/12/rhscl1-ga/
.. _default Python: https://www.archlinux.org/news/python-is-now-python-3/
.. _dubious: http://www.python.org/dev/peps/pep-0394/


When can we expect Python 2 to be a purely historical relic?
------------------------------------------------------------

Python 2 is still a good language. While I think Python 3 is a *better*
language (especially when it comes to the text model and error reporting),
we've deliberately designed the migration plan so users can update on
*their* timetable rather than ours (at least within a window of several
years), and we expect commercial redistributors to extend that timeline
even further.

I personally expect Python 2.7 to remain a reasonably common development
platform for at least another decade (that is, until 2024). The recent
public beta of Red Hat Enterprise Linux 7 uses Python 2.7 as the system
Python, and many library, framework and application developers base their
minimum supported version of Python on the system Python in RHEL (especially
since that also becomes the system Python in downstream rebuilds like CentOS
and Scientific Linux).

Aside from Blender, it appears most publishing and animation tools with
Python support (specifically Scribus, InkScape and AutoDesk tools like
Maya and MotionBuilder) are happy enough with Python 2.6 or 2.7 (AutoDesk
appear to be updating to 2.7 in 2014, Scribus and Inkspace already use 2.7).
This actually makes a fair bit of sense, especially for the commercial tools
from AutoDesk, since the Python support in these tools is there primarily to
manipulate the application data model and there aren't any major
improvements in Python 3 for that kind of use case, but still some risk of
breaking existing scripts if the application updates to Python 3.


.. _slow-uptake:

But uptake is so slow, doesn't this mean Python 3 is failing as a platform?
---------------------------------------------------------------------------

A common thread I have seen running through such declarations of "failure" is
people not quite understanding the key questions where the transition plan is
aiming to change the answers. These are the three key questions:

* "I am interested in learning Python. Should I learn Python 2 or Python 3?"
* "I am teaching a Python class. Should I teach Python 2 or Python 3?"
* "I am an experienced Python developer starting a new project. Should I
  use Python 2 or Python 3?"

At the start of the migration, the answer to all of those questions was
*obviously* "Python 2". Right now (March 2014), I believe the answer is
"Python 3.4, unless you have a compelling reason to choose Python 2 instead".
Possible compelling reasons include "I am teaching the course to maintainers
of an existing Python 2 code base", "We have a large in-house collection of
existing Python 2 only support libraries we want to reuse" and "I only use
the version of Python provided by my Linux distro vendor and they currently
only support Python 2" (although that last is also changing on the *vendor*
side - Red Hat now supports Python 3.3 through both Red Hat Software
Collections and as part of OpenShift Enterprise, and Canonical have
supported Python 3.2 since 12.04 LTS. SUSE don't support Python 3 yet, but
I'm told that support is expected to arrive as part of SLES 12).

Note the question that *isn't* on the list: "I have a large Python 2
application which is working well for me. Should I migrate it to Python 3?".

While OpenStack and some key Linux distributions have answered "Yes", we're
also happy enough for the answer to *that* question to remain "No" for the
time being. While it is likely that platform effects will eventually
shift even the answer to that question to "Yes" for the majority of users
(and Python 2 will have a much nicer exit strategy to a newer language than
COBOL ever did), the time frame for *that* change is a lot longer than the
five years that was projected for changing the default choice of Python
version for green field projects. That said, reducing or eliminating any
major remaining barriers to migration is an explicit design goal for
Python 3.5, in those cases where the change is also judged to be an
internal improvement within Python 3 (for example, the likely restoration
of binary interpolation support is motivated not just by making it easier
to migrate from Python 2, but also to make certain kinds of network
programming and other stream processing code easier to write in Python 3).

We're also happy enough if an application that *embeds* Python continues to
embed Python 2.7 rather than switching to embedding Python 3 - many embedding
use cases are primarily about using Python's basic procedural programming
support to manipulate the application data model, and those kinds of
operation haven't seen substantial changes in the Python 3 upgrade (in these
cases, the most significant change would likely be the one to make true
division on integers return a floating point result).

Several of the actions taken by the core development team have actually been
deliberately designed to keep conservative users *away* from Python 3 as a
way of providing time for the ecosystem to mature. Now, if Python 3 failed
to offer a desirable platform, nobody would care about this in the
slightest. Instead, what we currently see is the following:

* people coming up with great migration guides and utilities *independently*
  of the core development team. While `six`_ was created by a core
  developer (Benjamin Peterson), and `lib2to3` and the main porting guides
  are published by the core development team, `python-modernize`_ was created
  by Armin Ronacher (creator of Jinja2 and Flask), while `python-future`_
  was created by Ed Schofield based on that earlier work. Lennart Regebro
  has also done stellar work in creating an `in-depth guide to porting to
  Python 3 <http://python3porting.com/>`__
* Linux distributions aiming to make Python 2 an optional download and
  provide only Python 3 by default
* commercial Python redistributors ensuring that Python 3 is included as
  one of their supported offerings
* more constrained plugin ecosystems that use an embedded Python interpreter
  (like Blender, gcc, gdb and the Kate editor either adding Python 3
  support, or else migrating entirely from Python 2 to 3)
* developers lamenting the fact that they *want* to use Python 3, but are
  being blocked by various dependencies being missing, or because they
  currently use Python 2, and need to justify the cost of migration to their
  employer
* library and framework developers that hadn't already added Python 3 support
  for their own reasons being strongly encouraged by their users to offer it
  (sometimes in the form of code contributions, other times in the form of
  tracker issues, mailing list posts and blog entries)
* interesting new implementations/variants like MyPy and MicroPython taking
  advantage of the removal of legacy behaviour to target the leaner Python 3
  language design rather than trying to handle the full backwards
  compatibility implications of implementing Python 2
* developers complaining that the core development team isn't being
  aggressive enough in forcing the community to migrate promptly rather than
  allowing the migration to proceed at its own pace (!)

That last case is a relatively new one, and the difference in perspective
appears to be an instance of the classic early adopter/early majority divide
in platform adoption. The deliberately gentle migration plan is for the
benefit of the late adopters that drive Python's overall popularity, not
the early adopters that make up both the open source development community
and the (slightly) broader software development blogging community.

It's important to keep in mind that Python 2.6 (released October 2008) is
still one of the most widely deployed versions of Python, purely through
being the system Python in Red Hat Enterprise Linux 6 and its derivatives,
and usage of Python 2.4 (released November 2004) is non-trivial for the
same reason with respect to Red Hat Enterprise Linux 5. I expect there is a
similar effect from stable versions of Debian, Ubuntu LTS releases and SUSE
Linux Enterprise releases, but (by some strange coincidence) I'm not as
familiar with the Python versions and end-of-support dates for those as I
am with those for the products sold by my employer ;)

If we weren't getting complaints from the early adopter crowd about the pace
of the migration, *then* I'd be worried (because it would indicate they had
abandoned Python entirely and moved on to something else).

The other key point to keep in mind is that the available metrics on Python
3 adoption are quite limited. The three main quantitative options are to
analyse user agents on the Python Package Index, declarations of Python 3
support on PyPI and binary installer downloads for Mac OS X and Windows
from python.org.

The first of those is heavily dominated by *existing* Python 2 users, but
the trend in Python 3 usage is still upwards.

The second is based on manually recorded metadata rather than automated
version compatibility checking, but the stats as of January 2014 show
38.8k packages total, 26.5k claiming compatibility with *any* version of
Python and 3.5k claiming compatibility with Python 3. Of the top 200 most
downloaded packages, ~70% offer Python 3 support, with several of those
that are Python 2 only (such as sentry, graphite-web and supervisord)
typically being run as standalone services rather than as imported modules
that necessarily need to be using the same version of Python. Again, the
trend is upwards - I'm not aware of anyone *adding* Python 3 support, and
then removing it as imposing too much maintenance overhead (if using a
single source approach, as is now recommended for code that needs to support
both Python 2 and Python 3 simultaneously, the ongoing maintenance
requirement amounts to testing across multiple Python versions).

The last metric has now reached the point where Python 3 downloads outnumber
Python 2 downloads (54% vs 46%). The release of Python 3.4 should lead to
an uptick in all metrics, as the inclusion of pip makes it more likely
that workshop organisers will recommend the use of Python 3.4 over other
versions, as well as making it easier for new Python 3 users to discover
and start taking advantage of the Python package index. The Python 3
documentation has also been significantly improved in terms of introducing
new users to the broader Python ecosystem and helping to explain the many
tools that are available outside the standard library to solve various
problems.

The Python 3 ecosystem is definitely the smaller of the two at this point
in time (by a significant margin), but users that start with Python 3 should
be able to move to Python 2 easily enough if the need arises, and hopefully
with a clear idea of which parts of Python 2 are the modern recommended parts
that survived the transition to Python 3, and which parts are the legacy
cruft that only survives in the latest Python 2.x releases due to backwards
compatibility concerns.

For the inverse question relating to the concern that the existing migration
plan is too *aggressive*, see :ref:`abandoning-users`.


Is the ultimate success of Python 3 as a platform assured?
----------------------------------------------------------

At this point in time, I've very tempted to say "yes" (based on the
availability of commercial support from multiple independent vendors and
the availability of a majority of the core components of the Python 2
ecosystem), but I would moderate that to a "not quite yet, but I think the
outlook is very positive".

For me, with my Linux-and-infrastructure-software bias, the
tipping point will be Ubuntu and Fedora successfully making the transition
to only having Python 3 in their default install. Such a change will mean
a lot of key Linux infrastructure software is now Python 3 compatible, as
well as representing a significant statement of trust in the Python 3
platform by a couple of well respected organisations. It will also mean
that Python 3 will be more readily available than Python 2 on those
platforms in the future, and hence more likely to be used as the chosen
language variant for Python utility scripts, and hence increase the
attractiveness of supporting Python 3 for library and framework developers.

I also see the `ongoing migration
<https://wiki.openstack.org/wiki/Python3>`__ of OpenStack components from
being Python 2 only applications to being Python 3 compatible as highly
significant, as OpenStack is arguably one of the most notable Python
projects currently in existence in terms of spreading awareness outside
the traditional open stack and academic environs. In particular, if
OpenStack becomes a Python 3 application, then the plethora of cloud
provider developers and hardware vendor plugin developers employed
to work on it will all be learning Python 3 rather than Python 2.

The third notable milestone will be the degree of uptake of Python 3.4
amongst organisers of Python community workshops. Given that several of the
changes in 3.4 (such as including pip and adding the Scripts directory to
the PATH on Windows along with the main Python directory) were based
directly on concerns reported by those organisers, that outcome seems
likely, but can't be taken for granted at this point.

As far as the scientific community goes, they were amongst the earliest
adopters of Python 3 - I assume the reduced barriers to learnability were
something they appreciated, and the Unicode changes were not a problem that
caused them significant trouble.

I think the web development community has certainly had the roughest time of
it. Not only were the WSGI update discussions long and drawn out (and as
draining as any standards setting exercise), resulting in a compromise
solution that at least works but isn't simple to deal with, but they're also
the most directly affected by the core development team's wariness of
inadvertently reintroducing the Python 2 text model into Python 3,
since so many web related protocols are deliberately designed to be ASCII
compatible. However, even in the face of these issues, the major modern
Python web frameworks, libraries and database interfaces *do* support
Python 3, and the anticipated binary interpolation support in Python 3.5
will be aimed at carving out a subset of the binary interpolation
functionality in Python 2 that is considered consistent with the Python 3
text model. The adoption of ``asyncio`` as *the* standard framework for
asynchronous IO may also help the web development community resolve a
long standing issue with a lack of a standard way for web servers and web
frameworks to communicate regarding long lived client connections (such as
those needed for WebSockets support) - Victor Stinner's backport to Python
2 of the core callback based APIs may help with that, even though the
coroutine interface is different.

In the web space, I believe the main thing to watch is the availability of
Python 3 support for hosted application development. To take the three PaaS
providers that first come to mind, Heroku already supports Python 3.4, while
OpenShift Online currently provides Python 3.3. Google App Engine currently
offers only Python 2.7, and has not revealed any plans to offer Python 3 to
their users.


Python 3 is meant to make Unicode easier, so why is <X> harder?
---------------------------------------------------------------

At this point, the Python community as a whole has had more than 13 years
to get used to the Python 2 way of handling Unicode. For Python 3,
we've only had a production ready release available for around 4 and a
half years, and since some of the heaviest users of Unicode are the web
framework developers, and they've only had a stable WSGI target since the
release of 3.2, you can drop that down to just over 3 years of intensive
use by a wide range of developers with extensive practical experiencing
in handling Unicode (we have some *excellent* Unicode developers in the
core team, but feedback from a variety of sources is invaluable for a
change of this magnitude).

That feedback has already resulted in major improvements in the Unicode
support for the Python 3.2, 3.3, and 3.4 releases. With the
``codecs`` and ``email`` modules being brought into line, the recent
Python 3.4 release is the first one where the transition feels close to
being "done" to me in terms of coping with the full implications of a
strictly enforced distinction between binary and text data in the standard
library. However, I still expect that feedback process will continue
throughout the 3.x series, since "mostly done" and "done" aren't quite the
same thing, and attempting to closely integrate with POSIX systems that
may be using ASCII incompatible encodings while using a text model with
strict binary/text separation hasn't really been done before at Python's
scale (the JVM is UTF-16 based, but bypasses most OS provided services,
while other tools often choose the approach of just assuming that all bytes
are UTF-8 encoded, regardless of what they underlying OS claims).

In addition to the cases where blurring the binary/text distinction really
did make things simpler in Python 2, we're also forcing even developers in
strict ASCII-only environments to have to care about Unicode correctness,
or else explicitly tell the interpreter not to worry about it. This means
that Python 2 users that may have previously been able to ignore Unicode
issues may need to account for them properly when migrating to Python 3.

I've written more extensively on both of these topics in
:ref:`binary-protocols` and :ref:`py3k-text-files`.

The Python 3.5 release is currently looking like it will include some "make
ASCII compatible binary data as easy to work with as it is in Python 2"
changes, as well as further improvements to the handling of the impedance
mismatch with the POSIX "text" model.

..
   extra label to preserve link for the old question phrasing

.. _why-is-python-3-considered-a-better-language-to-teach-beginning-programmers:

Is Python 3 a better language to teach beginning programmers?
-------------------------------------------------------------

I believe so, yes. However, I also expect a lot of folks will still
want to continue on and learn Python 2 even if they learn Python 3 first
- I just think that for people that don't already know C, it will be
easier to start with Python 3, and then learn Python 2 (and the relevant
parts of C) in terms of the differences from Python 3 rather than
learning Python 2 directly and having to learn all those legacy details
at the same time as learning to program in the first place.

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
Python 3 releases, up to and including Python 3.4 (since that's the currently
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

In addition to the above changes, Python 3.4 includes `additional changes
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

The networking security changes are intermixed with the IO stack changes
for Unicode support, so backporting those, while technically possible, would
be a non-trivial task. Similarly, it's perhaps *possible* to backport the
implicit super change, but it would need to be separated from the other
backwards incompatible changes to the type system machinery.

There are some other notable changes in Python 3 that are of substantial
benefit when teaching new users (as well as for old hands), that technically
*could* be included in a Python 2.8 release if someone chose to create one,
but in practice such a release is unlikely to happen.

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
technically this could be backported, the implementation depends on the new
pure Python implementation of the import system, which in turn depends on
the Unicode friendly IO stack in Python 3, so backporting it would be far
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
    ImportError: No module named 'nspkg.b'

Python 3.3 also included some `minor <http://bugs.python.org/issue12265>`__
`improvements <http://bugs.python.org/issue12356>`__ to the error messages
produced when functions and methods are called with incorrect arguments.

The upcoming Python 3.4 release also aims to provide a significantly more
complete package for new users, by bundling the ``pip`` installer (see
:pep:`453`) and integrating it into the ``pyvenv`` virtual environment
creation utility (Python 3.3 already bundled the Python Launcher for Windows
with the Windows installers).

.. _room-for-improvement:

Is Python 3 more convenient than Python 2 in every respect?
-----------------------------------------------------------

At this point in time, not quite. Python 3.4 comes much closer to this
than Python 3.3 (which in turn was closer than 3.2, etc), but there are
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
``itervalues`` and ``iteritems`` methods from Python 2. There's also
a `current limitation <http://bugs.python.org/issue8743>`__ where builtin
sets don't interoperate properly with other instances of the Set ABCs
which I hope to get resolved for Python 3.5.

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
call to exclude binary operators), it's notable that the popular IPython
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
previously discussed on python-dev, python-ideas or the CPython issu
tracker include:

* taking the internal "text encoding" marking system added in Python 3.4
  and giving either it or a more general codec type description system a
  public API for use when developing custom codecs.
* making it easier to register custom codecs (preferably making use of
  the native namespace package support added in Python 3.3).
* introducing a string tainting mechanism that allows strings containing
  surrogate escaped bytes to be tagged with their encoding assumption and
  information about where the assumption was introduced. Attempting to
  process strings with incompatible encoding assumptions would then report
  both the incompatible assumptions and where they were introduced.
* creating a "strview" type that uses memoryview to provide a str-like
  interface to arbitrary binary buffers containing ASCII compatible
  protocol data.
* creating a hybrid type which behaves more like the Python 3
  bytestring, but rather than promoting itself to Unicode when encountering
  a Unicode string, instead ensure the result type matches the concrete type
  of the input. As with ``strview``, it would be designed specifically for
  handling ASCII compatible binary protocols rather than attempting to
  serve as a general purpose text container. A very early experimental
  prototype of such a type is `available
  <https://github.com/jeamland/asciicompat>`__.
* :pep:`460` and :pep:`461` are two different approaches to restoring
  support for *binary* interpolation that is to be source and semantically
  compatible for the use cases we actually want to support in Python 3 (
  neither proposal involves making the ``bytes`` type a hybrid type again,
  but instead proposes an interpolation mechanism that is suitable for
  working with binary formats that contain ASCII compatible segments).


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
as ``1atin-1`` decoded strings. This means that applications need to treat
these fields as wire protocol data (even though they claim to be text
based on their type), encode them back to bytes as ``latin-1``
and then decode them again using the *correct* encoding (as indicated
by other metadata).

The WSGI 1.1 spec is definitely a case of a "good enough" solution winning
a battle of attrition. I'm actually hugely appreciative of the web
development folks that put their time and energy both into creating the
WSGI 1.1 specification *and* into updating their tools to support it. Like
the Python core developers, most of the web development folks aren't in
a position to use Python 3 professionally, but *unlike* most of the core
developers, the kind of code they write falls squarely into the ASCII
compatible binary protocol space where Python 3 still has some significant
ground to make up relative to Python 2 in terms of usability (although
we've also converted our share of such code, just in bringing the standard
library up to scratch).


.. _posix-systems:

What's up with POSIX systems in Python 3?
-----------------------------------------

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
behaviour between environments with different configurations.

:pep:`383` added the surrogateescape error handler to cope with the fact that
the configuration settings on POSIX systems aren't always a reliable guide to
the *actual* encoding of the data you encounter. One of the most common
causes of problems is the seriously broken default encoding for the default
locale in POSIX (due to the age of the POSIX spec, that default is ASCII
rather than UTF-8). Bad default environments and environment forwarding in
ssh sessions are another source of problems, since an environment forwarded
from a client is not a reliable guide to the server configuration, and
if the ssh environment defaults to the C/POSIX locale, it will tell Python 3
to use ASCII as the default encoding rather than something more appropriate.

When surrogateescape was added, we considered enabling it for *every*
operating system interface by default (including file I/O), but the point
was once again made that this idea posed serious risks for silent data
corruption on Asian systems configured to use Shift-JIS, ISO-2022, or
other ASCII-incompatible encodings (European users were generally in a
safer position on this one, since Europe has substantially lower usage of
ASCII incompatible codecs than Asia does).

This means we've been judiciously adding surrogateescape to interfaces as
we decide the increase in convenience justifies any increased risk of
data corruption. The next likely `candidate for change
<http://bugs.python.org/issue19977>`__ is ``sys.stdin`` and ``sys.stdout`` on
POSIX systems that claim that we should be using ``ascii`` as the default
encoding. Such a result almost certainly indicates a configuration error
in the environment, but using ascii+surrogateescape in such cases should
make for a more usable result than the current approach of ascii+strict.
There's still some risk of silent data corruption in the face of ASCII
incompatible encodings, but the assumption is that systems that are
configured with a non-ASCII compatible encoding should already have
relatively robust configurations that avoid ever relying on the default POSIX
locale. This change has already been merged for Python 3.5, and is still
under consideration for inclusion in the Python 3.4.1 maintenance release.

This is an area where we're genuinely open to the case being made for
different defaults, or additional command line or environment variable
configuration options. POSIX is just seriously broken in this space, and
we're having to trade-off user convenience against the risk of silent data
corruption - that means the "right answer" is *not* obvious, and any PEP
proposing a change needs to properly account for the rationale behind the
current decision (which may unfortunately involve some digging through the
python-3000, python-dev and python-ideas mailing list archives and the
CPython issue tracker, as it turns out some of the rationale was apparently
considered common knowledge when PEPs like :pep:`3138`, :pep:`3116` and
:pep:`383` were written, and hence not recorded as a specific part of the
PEPs themselves).


What changes in Python 3 have been made specifically to simplify migration?
---------------------------------------------------------------------------

The biggest change made specifically to ease migration from Python 2 was the
reintroduction of Unicode literals in Python 3.3 (in :pep:`414`). This
allows developers supporting both Python 2 and 3 in a single code base to
easily distinguish binary literals, text literals and native strings, as
``b"binary"`` means bytes in Python 3 and str in Python 2, ``u"text"``
means str in Python 3.3+ and unicode in Python 2, while ``"native"`` means
str in both Python 2 and 3.

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

The `landing page for the Python documentation <http://docs.python.org>`__
was also switched some time ago to display the Python 3 documentation by
default, although deep links still refer to the Python 2 documentation in
order to preserve the accuracy of third party references (see :pep:`430`
for details).


What future changes in Python 3 are expected to further simplify migration?
---------------------------------------------------------------------------

With Python 3.4 including many changes focused on improving the experience
for new users (such as including pip by default, more secure default
settings for various operations and adding a basic statistics module to
the standard library) to help achieve the goal of making Python 3 the
preferred choice for new users and projects, it is expected that the
Python 3.5 development cycle over 2014 and 2015 will include a concerted
effort to address any other remaining significant barriers to migration
from Python 2.

One such barrier is the fact that Python 3 (up to and including Python 3.4)
doesn't provide an interpolation mechanism for binary formats that
include ASCII compatible segments. Instead, binary data must be collated as
a list and merged using bytes.join, formatted using the ``struct`` module,
or interpolated as text and then encoded using a consistent encoding. While
these methods are more obviously structurally correct and work with
arbitrary binary data, there are still cases when working with data formats
containing ASCII compatible segments where a dedicated binary interpolation
mechanism would be significantly more convenient.

After his experience working with networking protocols in Python 3
during the development of ``asyncio``, and in response to the identification
of the lack of such an interpolation mechanism that directly produces ASCII
compatible binary data as an issue for porting at least Twisted and
Mercurial to Python 3, Guido has come to the conclusion that bringing back
such a feature fits within the same category as the other methods on bytes
objects that assume ASCII compatibility, rather than being a reintroduction
of the implicit interoperability between text and binary data that is a
significant cause of latent encoding related defects in Python 2. We have
also been using Python 3 for long enough now to feel that the desire for
this feature is based in a genuine use case driven need, rather than merely
being a holdover from the more lenient Python 2 text model (which was a
significant concern in the early days of Python 3, when even the core
development team was still getting used to the full implications of the
stricter separation between binary and text data in Python 3).

While Guido has yet to make a pronouncement, the general tenor of the
discussions so far suggests to me that something in the general vein of
:pep:`461` is likely to be approved for inclusion in Python 3.5, even
though the specific details haven't been finalized.

It is also likely (although not yet certain) that the relative release
dates of the final regular maintenance release of Python 2.7 and the
initial release of Python 3.5 in 2015 will be adjusted so that Python 3.5
is released prior to Python 2.7 entering security fix only mode.


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

Finally, Python 3.3 has converted the bulk of the import system over to pure
Python code so that all implementations can finally start sharing a common
import implementation. Some work will be needed from each implementation to
work out how to bootstrap that code into the running interpreter (this was
one of the trickiest aspects for CPython), but once that hurdle is passed
all future import changes should be supported with minimal additional effort.

All that said, there's often a stark difference in the near term *goals* of
the core development team and the developers for other implementations.
Criticism of the Python 3 project has been most vocal from a number of
PyPy core developers, and that makes sense when you consider that one of
the core aims of PyPy is to provide a better runtime for *existing* Python
applications. That means their focus is likely to remain on Python 2.7 and
providing compatibility with the scientific Python stack for some time to
come.

However, the reasons Armin Rigo originally abandoned psyco to instead
initiate the PyPy project are *very* similar to the reasons Guido and the
rest of the core development team put the Python 2 runtime into maintenance
mode and started focusing feature development efforts on the Python 3
runtime instead: there were things we wanted to do that were at best
impractical, and in some cases impossible, within the backwards
compatibility constraints of Python 2. The key difference is that where
Armin was constrained solely by the design of the CPython runtime
implementation, Guido was also constrained by the language definition.

The similarity between the two cases can be seen in the fact that PyPy
adoption is limited by both the ubiquity of CPython and the need to
support key extension modules (hence the numpypy project), and Python 3
adoption is similarly dependent on growing the ecosystem to match that of
CPython 2.7 (although the benefits of making things easier for people that
aren't full time programmers meant that the scientific Python community were
amongst the earlier adopters of Python 3).

Unlike Jython and IronPython, neither Python 3 nor PyPy offer
an integration story with a pre-existing third party runtime (the JVM for
Jython and the CLR for IronPython) that makes them especially attractive
to a specific subset of users - this means that both Python 3 and PyPy
need to leverage the existing Python 2 ecosystem rather than trying to
create a new ecosystem from scratch. (The Python 2 ecosystem is
significant enough in the scientific space that the designers of the new
scientific language Julia chose to include native integration with Python
in addition to C and FORTRAN).

It's also notable that the Python 3 compatible branch of PyPy is both
well funded and well advanced, *despite* the PyPy team's documented
reservations.

Jython is in a similar situation to PyPy, but a bit further behind -
their development efforts are currently focused on getting their
currently-in-beta Python 2.7 support to a full release, and there is also
some significant work happening on JyNI (which, like PyPy's numpypy project,
aims to allow the use of the scientific Python stack from the JVM).

The IronPython folks are `looking to have
<http://blog.jdhardy.ca/2013/06/ironpython-3-todo.html>`__ a Python 3
compatible version available by mid 2014. IronClad already supports the
use of `scientific libraries from IronPython
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
of 2.7 is slated to revert to security-fix only mode in July 2015, even
after python-dev upstream maintenance ends, Python 2.6 will still be
supported by enterprise Linux vendors until at least 2020, while Python 2.7
will be supported until at least 2024. On Windows and Mac OS X, commercial
Python redistributors are also likely to fill the support gap once upstream
maintenance ends.

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

An important thing to understand for anyone hoping to convince the core
development team to change direction in regards to Python 3 development
and promotion is to know that mere words aren't enough, it's going to take
action. That action is defined in :pep:`404`: creating a Python 2.8 release
(under a different name, however, since ``Python`` refers specifically to
the language versions endorsed by the core development team) and convincing
people to use it.

If that happens, I still expect the most likely outcome to be for the
majority of currently happy Python 2 users to stick with Python 2.7, and
perhaps some of the PyPI modules that are backports from the Python standard
library. Most of the genuinely interesting changes between Python 2 and even
Python 3.4 are either backwards incompatible themselves, or else dependent
on a backwards incompatible change.

Migrating to a new Python version even within the Python 2.x series is
generally treated as a major change requiring substantial compatibility
testing (Linux distributions, for example, typically don't change the
major version of the system Python for the full lifecycle of a given
release). Migrating to a new version maintained by a different set of
developers would need an even more compelling justification, and it seems
unlikely enough features can be effectively backported from Python 3 to
Python 2 to provide that justification.

So far, we haven't even seen a concerted effort to create a community
"Python 2.7+" release that bundles all of the available 3.x backport
libraries with the base 2.7 distribution (which would be a much simpler
project), so the prospects for a new Python 2.8 fork that actually
backports compatible changes to the interpreter core seem limited. Heck,
until I added it to the `Python 2 or Python 3`_ page on the Python wiki,
nobody had even put in the minimal effort needed to create a shared list
of the standard library additions in 3.x that were also available on PyPI.
This suggests that users that desire Python 3 features in Python 2 are
willing and able to do the backports themselves in the cases where it
matters, and this has the added benefit of potentially decoupling future
updates of those modules from the CPython upgrade cycle (which is
critical for software that aims to support multiple versions with a
minimum of effort).

A crash in general Python adoption would also make us change our minds,
but Python is working its way into more and more niches *despite* the
Python 3 transition, so the only case that can be made is "adoption would
be growing even faster without Python 3 in the picture", which is a hard
statement to prove (particularly when we suspect that at least some of
the growth in countries where English is not the primary spoken language
is likely to be *because* of Python 3 rather than in spite of it, and that
the Python 3 text model is in a much better position to serve as a bridge
between the POSIX text model and the JVM text model than the Python 2
model ever was).

A third alternative that would make us seriously question our current
strategy is if community workshops aimed at new programmers chose not to
switch to recommending Python 3.4 by default after it is released, *despite*
the significant carrots of ``pip`` being provided by default on Windows and
Mac OS X and integrated into ``pyvenv`` on all platforms, the inclusion
of :mod:`pathlib`, :mod:`statistics`, :mod:`asyncio`, more secure default
settings for SSL/TLS, `etc <http://docs.python.org/3.4/whatsnew/3.4.html>`__.


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
has an additional 3 years of feature development under its belt relative to
the Python 2 series.

There *are* parts of the Python 3 standard library that are also useful in
Python 2. In those cases, they're frequently available as backports on
the Python Package Index (including even a backport of the new asynchronous
IO infrastructure).

I think the other aspect that is often missed in these discussions is that
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

Python 2.6 compatibility is still required more than 6 years after its
original release, and this likely won't be dropped until after a CentOS 7
release is available.

I believe Twisted has one of *the* most conservative user bases in the
Python community, and I consider this one of the main reasons we see this
general pattern of only dropping support for an older release 6-7 years
after it was first made available. That's also why I consider the Twisted
developers a key audience for any increases in the scope of single source
support in Python 3.5 (and their support for the idea is certainly one of
the factors behind the likely return of binary interpolation support).

That's the way the path to Python 3 will be smoothed at this point: by
identifying blockers to migration and knocking them down, one by one. The
PSF has helped fund the migration of some key libraries. Barry Warsaw drove
a fair amount of Python 3 migration work for Ubuntu at Canonical. Victor
Stinner is working hard to encourage and support the OpenStack migration. I
have been offering advice and encouragement to Bohuslav Kabrda (the main
instigator of Fedora's migration to Python 3), as well as helping out with
Fedora policy recommendations on supporting parallel Python 2 and 3 stacks (I
have actually had very little to do with Red Hat's efforts to support Python
3 overall, as I haven't needed to. Things like Python 3 support in Red Hat
Software Collections and OpenShift Online happened because other folks at
Red Hat made sure they happened). Guido approved the restoration of Unicode
literal support after web framework developers realised they couldn't mask
that particular change for their users, and is likely to approve the
restoration of binary interpolation support. I went through and made the
binary transform codecs that had been restored in Python 3.2 easier to
discover and use effectively in Python 3.4. R. David Murray put in a lot
of time and effort to actually handle Unicode sensibly in the ``email``
module.


Aren't the Stackless developers talking about creating a Stackless 2.8?
-----------------------------------------------------------------------

Yes, they are - they're considering it specifically in the context of
creating a new version of Stackless for Windows that is `built with Visual
Studio 2010
<https://mail.python.org/pipermail/python-dev/2013-November/130421.html>`__
rather than Visual Studio 2008. Due to the incompatible C runtimes in the
two versions, such a change will render affected Stackless builds
incompatible with all Windows C extensions built to be compatible with
CPython 2.7, and the way such a binary extension incompatibility has
historically been indicated is through incrementing the second digit in
the Python version.

With the cooperation of the CPython core development team and interested
parties from Microsoft, they've explored various alternatives (including
talking to the Microsoft Visual Studio and MSVC runtime developers about
ways to support running both the 2008 and 2010 runtimes in the same
process), but, aside from creating a new binary incompatible version of
Stackless and incrementing the implementation version number appropriately,
there currently doesn't seem to be an immediately practical way for the
Stackless developers to support their users that are asking for Visual
Studio 2010 compatible builds.

At the request of the core development team, one key aspect of the approach
the Stackless team are `currently looking at taking
<http://stackless.com/pipermail/stackless/2013-November/005934.html>`__
is to consistently use the name "Stackless 2.8" and avoid referring
to the new variant as a different version of Python.

This is the *one* case where I can see any kind of continued feature
development based on the Python 2 series gaining any traction - the
Stackless folks already have the infrastructure and community to
maintain a CPython fork (as they have been doing it for years),
and have earned justified respect and trust through powering EVE Online and
CCP's other games, as well as by providing the technical foundation for the
``greenlets`` extension module in CPython. Since it's only a small step
from maintaining Stackless Python 2.7 as a CPython variant with slightly
different runtime semantics but fully consistent syntax to creating a
Stackless 2.8 that also deviates slightly in syntax and standard library
contents (by adding features from Python 3), the Stackless team are
considering doing exactly that.

I trust the Stackless folks to be responsible stewards of Stackless 2.8
(for example, by preserving full Python 2.7 compatibility at the syntactic
and C API level), so if this approach garners them additional Python 2
users that are interested in any Python 3 features they decide to backport,
more power to them - I like seeing good things happen to people I consider
colleagues, and more users and support for their platform would be a good
thing :)


Aren't you concerned Python 2 users will abandon Python over this?
------------------------------------------------------------------

Certainly - a change of this magnitude is sufficiently disruptive that
many members of the Python community are legitimately upset at the impact
it is having on them.

This is particularly the case for users that have never personally been
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
support from python-dev.  We're not *opposed* to such efforts - it's merely the
case that we aren't interested in doing them ourselves, and are unlikely to
devote significant amounts of time to assisting those that *are* interested.

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
frame (at least by open source volunteer supported project standards)
for the user community to make the transition. Even after full
maintenance of Python 2.7 ends in 2015, source only security
releases will continue for some time, and, as noted above, I expect
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
* Approach the PSF or the core development team regarding funding the
  creation of a Python 2.8 release with selected backwards compatible
  feature backports from Python 3 that can't be readily backported as
  independent modules
* Fork Python 2 to add the missing features for their own benefit
* Migrate to a language other than Python

The first three of those approaches are all fully supported by python-dev.
Many standard library additions in Python 3 started as modules on PyPI and
thus remain available to Python 2 users. For other cases, such as ``unittest``
or ``configparser``, the respective standard library maintainer also maintains
a PyPI backport.

The fourth choice seems rather unlikely, but could be an interesting
conversation to have.

As noted above, it currently seems likely that CCP and the Stackless
community will be pursuing the fifth option. That's the power of open
source - the Stackless fork has already been maintained for years to
natively provide the behaviour that was brought back to CPython as the
``greenlets`` extension module, and the permissive licensing of the CPython
source code means they're also free to incorporate additional changes
from Python 3 if they choose to. I (and I think most others) have always
counted the Stackless developers and their users as members of the Python
community, and adding a few Python 3 features into Stackless 2.8 won't do
anything to change that.

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
fail to correctly close resources on failure. For Python 3.3, it has finally
been replaced with a superior incremental ``contextlib.ExitStack`` API which
should support similar functionality without being anywhere near as error
prone.

Secondly, code level deprecation warnings are now silenced by default. The
expectation is that test frameworks and test suites will enable them (so
developers can fix them), while they won't be readily visible to end users
of applications that happen to be written in Python.

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

The anticipated restoration of some form of binary interpolation support in
Python 3.5 is similar intended to increase the size of the common subset of
Python 2 and Python 3 in a way that makes it easier for developers to migrate
to the new version of the language (as well as being a useful new feature
for Python 3 in its own right).

If you want to keep track of Python's development and get some idea of
what's coming down the pipe in the future, it's all
`available on the internet`_.

.. _available on the internet: http://docs.python.org/devguide/communication.html


But, but, surely fixing the GIL is more important than fixing Unicode...
------------------------------------------------------------------------

While this complaint isn't really Python 3 specific, it comes up often
enough that I wanted to put in writing why most of the core development
team simply don't see the GIL as a significant problem for the typical
workloads faced by Python applications (yes, this is a circular argument
- more on that below).

Earlier versions of this section were needlessly dismissive of the
concerns of those that wish to combine their preference for programming
in Python with their preference for using threads to exploit the
capabilities of multiple cores on a single machine. In the interests of
clear communication, the text has been rewritten in a more constructive
tone. If you wish to see the snarkier early versions, they're
available in the `source repo`_ for this site.

.. _source repo: https://bitbucket.org/ncoghlan/misc/history-node/default/notes/python3/questions_and_answers.rst?at=default


Why is using a Global Interpreter Lock (GIL) a problem?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The key issue with Python implementations that rely on a GIL (most notably
CPython and PyPy) is that it makes them entirely unsuitable for cases where
a developer wishes to:

* use shared memory threading to exploit multiple cores on a single machine
* write their entire application in Python, including CPU bound elements
* use CPython or PyPy as their interpreter

This combination of requirements simply doesn't work - the GIL effectively
restricts bytecode execution to a single core, thus rendering pure Python
threads an ineffective tool for distributing CPU bound work across multiple
cores.

At this point, one of those requirements has to give. The developer has to
either:

* use a concurrency technique other than shared memory threading
* move parts of the application out into non-Python code (the path taken
  by the NumPy/SciPy community, all Cython users and many other people
  using Python as a glue language to bind disparate components together)
* use a Python implementation that doesn't rely on a GIL (while the main
  purpose of Jython and IronPython is to interoperate with other JVM and
  CLR components, they are also free threaded thanks to the cross-platform
  threading primitives provide by the underlying virtual machines)
* use a language other than Python

Many Python developers find this annoying - they want to use threads *and*
they want to use Python, but they have the CPython core developers in their
way saying "Sorry, we don't support that style of programming".


What alternative approaches are available?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Assuming that a free-threaded Python implementation like Jython or IronPython
isn't suitable for a given application, then there are two main approaches
to handling distribution of CPU bound Python workloads in the presence of
a GIL. Which one will be more appropriate will depend on the specific task
and developer preference.

The approach most directly supported by python-dev is the use of
process-based concurrency rather than thread-based concurrency. All
major threading APIs have a process-based equivalent, allowing threading
to be used for concurrent synchronous IO calls, while multiple processes can
be used for concurrent CPU bound calculations in Python code. The
strict memory separation imposed by using multiple processes also makes
it much easier to avoid many of the common traps of multi-threaded code.
As another added bonus, for applications which would benefit from scaling
beyond the limits of a single machine, starting with multiple processes
means that any reliance on shared memory will already be gone, removing
one of the major stumbling blocks to distributed processing.

The major alternative approach promoted by the community is best represented
by `Cython`_. Cython is a Python superset designed to be compiled down to
CPython C extension modules. One of the features Cython offers (as is
possible from any C extension module) is the ability to explicitly release
the GIL around a section of code. By releasing the GIL in this fashion,
Cython code can fully exploit all cores on a machine for computationally
intensive sections of the code, while retaining all the benefits of Python
for other parts of the application.

`Numba`_ is another tool in a similar vein - it uses LLVM to convert Python
code to machine code that can run with the GIL released (as well as
exploiting vector operations provided by the CPU when appopriate).

This approach also works when calling out to *any* code written in other
languages: release the GIL when handing over control to the external library,
reacquire it when returning control to the Python interpreter.

.. _Cython: http://www.cython.org/
.. _release the GIL: http://docs.cython.org/src/userguide/external_C_code.html#acquiring-and-releasing-the-gil
.. _Numba: http://numba.pydata.org/


Why doesn't this limitation really bother the core development team?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In my case, I came to Python by way of the unittest module: I needed to
write a better test suite for a C++ library that communicated with a
custom DSP application, and by using SWIG and the Python unittest module
I was able to do so easily. Using Python for the test suite also let me
easily play audio files out of the test hardware into the DSP unit being
tested. Still in the test domain, I later used Python to communicate with
serial hardware (and push data through serial circuits and analyse what
came back), write prototype clients to ensure new hardware systems were full
functional replacements for old ones and write hardware simulators to allow
more integration errors could be caught during software development rather
than only after new releases were deployed to the test lab that had real
hardware available.

Other current Python users are often in a similar boat - we're using Python
as an orchestration language, getting other pieces of hardware and software
to play nice, so the Python components just need to be "fast enough", and
allow multiple *external* operations to occur in parallel, rather than
necessarily needing to run Python bytecode operations concurrently.

This is certainly true of the scientific community, where the heavy numeric
lifting is all done in C or FORTRAN, and the Python components are there to
make everything hang together in a way humans can read relatively easily.

In the case of web development, while the speed of the application server
may become a determining factor at truly massive scale, smaller applications
are likely to gain more by adding a Varnish caching server in front of the
application, and a memory cache between the application and its
database before the application server itself is likely to become the
bottleneck.

This means for the kind of use case where Python is primarily playing an
orchestration role, as well as those where the application is IO bound
rather than CPU bound, free threading doesn't really provide a lot of
benefit - the Python code was never the bottleneck in the first place, so
focusing optimisation efforts on the Python runtime doesn't make sense.

Instead, people drop out of pure Python code into an environment that is
vastly easier to optimise and already supports free threading. This may be
hand written C or C++ code, it may be something with Pythonic syntax but
reduced dynamism like Cython or Numba, or it may be another more static
language on a preexisting runtime like the JVM or the CLR, but however it
is achieve, the level shift allows optimisations and parallelism to be
applied at the places where they will do the most good for the overall
speed of the application.


Why isn't "just remove the GIL" the obvious answer?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Removing the GIL *is* the obvious answer. The problem with this phrase is
the "just" part, not the "remove the GIL" part.

One of the key issues with threading models built on shared
non-transactional memory is that they are a broken approach to general
purpose concurrency. Armin Rigo has explained that far more eloquently
than I can in the introduction to his `Software Transactional Memory`_ work
for PyPy, but the general idea is that threading is to concurrency as the
Python 2 Unicode model is to text handling - it works great a lot of the
time, but if you make a mistake (which is inevitable in any non-trivial
program) the consequences are unpredictable (and often catastrophic from an
application stability point of view), and the resulting situations are
frequently a nightmare to debug.

The advantages of GIL-style coarse grained locking for the CPython
interpreter implementation are that it makes naively threaded code
more likely to run correctly, greatly simplifies the interpreter
implementation (thus increasing general reliability and ease of
porting to other platforms) and has almost zero overhead when
running in single-threaded mode for simple scripts or event driven
applications which don't need to interact with any synchronous APIs (as
the GIL is not initialised until the threading support is imported,
or initialised via the C API, the only overhead is a boolean
check to see if the GIL has been created).

The CPython development team have long had a (previously unwritten) list
of requirements that any free-threaded Python variant must meet before
it could be considered for incorporation into the reference interpreter:

* must not substantially slow down single-threaded applications
* must not substantially increase latency times in IO bound applications
* threading support must remain optional to ease porting to platforms
  with no (or broken) threading primitives
* must minimise breakage of current end user Python code that implicitly
  relies on the coarse-grained locking provided by the GIL (I recommend
  consulting Armin's STM introduction on the challenges posed by this)
* must remain compatible with existing third party C extensions that rely
  on refcounting and the GIL (I recommend consulting with the cpyext
  and IronClad developers both on the difficulty of meeting this
  requirement, and the lack of interest many parts of the community have
  in any Python implementation that doesn't abide by it)
* must achieve all of these without reducing the number of supported
  platforms for CPython, or substantially increasing the difficulty of
  porting the CPython interpreter to a new platform (I recommend consulting
  with the JVM and CLR developers on the difficulty of producing and
  maintaining high performance cross platform threading primitives).

It is important to keep in mind that CPython already has a massive user
base that doesn't find the GIL to be a problem, or else find it to be a
problem that is easy to work around. Core development efforts in the
concurrency arena have focused on better serving the needs of those users
by providing better primitives for easily distributing work across multiple
processes. Examples of this approach include the initial incorporation of
the :mod:`multiprocessing` module, which aims to make it easy to migrate
from threaded code to multiprocess code, along with the addition of the
:mod:`concurrent.futures` module in Python 3.2, which aims to make it easy to
take serial code and dispatch it to multiple threads (for IO bound
operations) or multiple processes (for CPU bound operations) and the
:mod:`asyncio` module in Python 3.4 (which provides full support for
explicit asynchronous programming in the standard library).

For IO bound code (with no CPU bound threads present), or, equivalently, code
that invokes external libraries to perform calculations (as is the case for
most serious number crunching code, such as that using NumPy and/or Cython),
the GIL does place an additional constraint on the application, but one that
is typically easy to satisfy: a single core must be able to handle all
Python execution on the machine, with other cores either left idle
(IO bound systems) or busy handling calculations (external library
invocations). If that is not the case, then multiple interpreter processes
will be needed, just as they are in the case of any CPU bound Python threads.

For seriously concurrent problems, a free threaded interpreter also doesn't
help much, as it is desired to scale not only to multiple cores on a single
machine, but to multiple *machines*.
As soon as a second machine enters the picture, threading based concurrency
can't help you: you need to use a concurrency model (such as message passing
or a shared datastore) that allows information to be passed between
processes, either on a single machine or on multiple machines.

CPython also has another problem that limits the effectiveness of removing
the GIL: we use a reference counting garbage collector with cycle detection.
This hurts free-threading in two major ways: firstly, any free-threaded
solution that retains the reference counting GC will still need a global
lock that protects the integrity of the reference counts; secondly, switching
threads in the CPython runtime will mean updating the reference counts on a
whole new working set of objects, almost certainly blowing the CPU cache
and losing a bunch of the speed benefits gained from making more effective
use of multiple cores.

So the reference counting GC would likely have to go as well, or be replaced
with an allocation model that uses a separate heap per thread by default,
creating yet *another* compatibility problem for C extensions.

These various factors all combine to explain why there's no strong motivation
to implement fine-grained locking in CPython in the near term:

* a coarse-grained lock makes threaded code behave in a less surprising
  fashion
* a coarse-grained lock makes the implementation substantially simpler
* a coarse-grained lock imposes negligible overhead on the scripting use case
* fine-grained locking provides no benefits to single-threaded code (such as
  end user scripts)
* fine-grained locking may break end user code that implicitly relies on
  CPython's use of coarse grained locking
* fine-grained locking provides minimal benefits to event-based code
  that uses threads solely to provide asynchronous access to external
  synchronous interfaces (such as web applications using an event based
  framework like Twisted or gevent, or GUI applications using the GUI event
  loop)
* fine-grained locking provides minimal benefits to code that
  uses other languages like Cython, C or Fortran for the serious number
  crunching (as is common in the NumPy/SciPy community)
* fine-grained locking provides no substantial benefits to code that needs
  to scale to multiple machines, and thus cannot rely on shared memory for
  data exchange
* a refcounting GC doesn't really play well with fine-grained locking
  (primarily from the point of view of high contention on the lock that
  protects the integrity of the refcounts, but also the bad effects on
  caching when switching to different threads and writing to the refcount
  fields of a new working set of objects)
* increasing the complexity of the core interpreter implementation for any
  reason always poses risks to maintainability, reliability and portability

Given the dubious payoff, and the wide array of effective alternatives, is
it really that surprising that the GIL isn't seen as the big problem it
is often made out to be? Sure, it's not ideal, and if a portable, reliable,
maintainable free-threaded implementation was dropped in our laps we'd
certainly seriously consider adopting it, but we're not an OS kernel -
we have the option of farming work out to a separate process if the GIL
is a problem for a particular workload.

It isn't that a free threaded Python implementation isn't possible (Jython
and IronPython prove that), it's that free threaded virtual machines are
hard to write correctly in the first place and are harder to maintain once
implemented. Linux had the "Big Kernel Lock" for years for basically the
same reason. For CPython, any engineering effort directed towards free
threading support is engineering effort that isn't being directed
somewhere else. The current core development team don't consider
that a good trade-off and, to date, nobody else has successfully
taken up the standing challenge to try and prove us wrong.

Some significant work did go into optimising the GIL behaviour for CPython
3.2, and further tweaks are possible in the future as more applications are
ported to Python 3 and get to experience the results of that work, but
more extensive changes to the CPython threading model are highly likely to
fail the risk/reward trade-off.

In the meantime, the core development term prefer a clear category error
("if your requirements include both X and Y, don't use Z") over the potential
reliability and maintainability issues associated with adopting a free
threaded interpreter design.


What does the future look like for concurrency in Python?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

My own long term hope is that Armin Rigo's research into `Software
Transactional Memory`_ eventually bears fruit. I know he has some thoughts
on how the concepts he is exploring in PyPy could be translated back to
CPython, but even if that doesn't pan out, it's very easy to envision a
future where CPython is used for command line utilities (which are generally
single threaded and often so short running that the PyPy JIT never gets a
chance to warm up) and embedded systems, while PyPy takes over the execution
of long running scripts and applications, letting them run substantially
faster and span multiple cores without requiring any modifications to the
Python code. Splitting the role of the two VMs in that fashion would allow
each to be optimised appropriately rather than having to make trade-offs that
attempt to balance the starkly different needs of the various use cases.

I also expect we'll continue to add APIs and features designed to make it
easier to farm work out to other processes (for example, the new iteration
of the `pickle protocol`_ in Python 3.4 includes the ability to
unpickle unbound methods by name, which should allow them to be used
with the multiprocessing APIs).

Another potentially interesting project is `Trent Nelson's work`_ on using
memory page locking to permit the creation of "shared nothing" worker
threads, that would permit the use of a more Rust-style memory model within
CPython (note that the descriptions of a number of other projects in the
linked presentation are inaccurate. In particular, most Python async IO
libraries, including both Twisted and asyncio, use IOCP on Windows).

Alex Gaynor also pointed out `some interesting research (PDF)
<http://researcher.watson.ibm.com/researcher/files/jp-ODAIRA/PPoPP2014_RubyGILHTM.pdf>`__
into replacing Ruby's Giant VM Lock (the equivalent to CPython's GIL in
CRuby, aka the Matz Ruby Interpreter) with appropriate use of Hardware
Transactional Memory, which may also prove relevant to CPython as HTM
capable hardware becomes more common. (However, note the difficulties that
the refcounting in MRI caused the researchers - CPython is likely to have
exactly the same problem, with a well established history of attempting to
eliminate and then emulate the refcounting causing major compatibility
problems with extension modules).

Sarah Mount reminded me in early 2014 of some speculative ideas I had
regarding the possibility of `refining CPython's subinterpreter
<http://www.curiousefficiency.org/posts/2012/07/volunteer-supported-free-threaded-cross.html>`__
concept to make it a first class language feature that offered true
in-process concurrency in a way that didn't break compatibility with
C extension modules (well, at least not any more than using subinterpreters
in combination with extensions that call back into Python from C created
threads already breaks it).

As far as a free-threaded CPython implementation goes, that seems unlikely
in the absence of a corporate sponsor willing to pay for the development and
maintenance of the necessary high performance cross-platform threading
primitives, their incorporation into a fork of CPython, and the extensive
testing needed to ensure compatibility with the existing CPython ecosystem,
and then persuading python-dev to accept the additional maintenance burden
imposed by accepting such changes back into the reference implementation.

One of the key issues with CPython in particular is that it's not only
the Global Interpreter Lock that is threading unfriendly, but also the
reference counting GC. An effectively free-threaded interpreter based on
CPython would likely need to replace the GC as well, which is why other
interpreter implementations like Jython, IronPython or PyPy are better
positioned in this regard (since they already use garbage collectors based
on mechanisms other than reference counting).

I personally expect most potential corporate sponsors with a vested interest
in Python to spend their money more cost effectively and just tell their
engineers to use multiple processes instead of threads, or else to
contribute to sponsoring Armin's work on `Software Transactional Memory`_.

.. _Software Transactional Memory: http://morepypy.blogspot.com.au/2011/08/we-need-software-transactional-memory.html
.. _further tweaks: http://bugs.python.org/issue7946
.. _pickle protocol: http://www.python.org/dev/peps/pep-3154/
.. _Trent Nelson's work: http://vimeo.com/79539317


Well, why not just add JIT compilation, then?
---------------------------------------------

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

The efforts of the first five years of Python 3 deployment have been about
positioning it to start crossing that gap between early adopters and more
conservative users. Those pieces are starting to fall into place,
especially as enterprise Linux vendors start bringing supported Python 3
offerings to market.

This means that while conservative users that are *already* using Python are
likely to stick with Python 2 for the time being ("if it isn't broken for us,
why change it?"), *new* conservative users will see a fully supported
environment, and 3 is a higher number than 2, even if the ecosystem still has
quite a bit of catching up to do (conservative users aren't going to be
downloading much directly from PyPI either - they often prefer to outsource
that kind of filtering to software vendors rather than doing it themselves).
