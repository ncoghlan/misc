.. _py3k-text-files:

Processing Text Files in Python 3
=================================

A recent discussion on the python-ideas mailing list made it clear that we
(i.e. the core Python developers) need to provide some clearer guidance on
how to handle text processing tasks that trigger exceptions by default in
Python 3, but were previously swept under the rug by Python 2's blithe
assumption that all files are encoded in "latin-1".

While we'll have something in the official docs `before too long`_, this is
my own preliminary attempt at summarising the options for processing text
files, and the various trade-offs between them.

.. _before too long: http://bugs.python.org/issue13997

.. contents::
   :local:
   :backlinks: top


What changed in Python 3?
-------------------------

The obvious question to ask is what changed in Python 3 so that the common
approaches that developers used to use for text processing in Python 2 have
now started to throw ``UnicodeDecodeError`` and ``UnicodeEncodeError`` in
Python 3.

The key difference is that the default text processing behaviour in Python 3
aims to detect text encoding problems as early as possible - either when
reading improperly encoded text (indicated by ``UnicodeDecodeError``) or when
being asked to write out a text sequence that cannot be correctly represented
in the target encoding (indicated by ``UnicodeEncodeError``).

This contrasts with the Python 2 approach which allowed data corruption by
default and strict correctness checks had to be requested explicitly. That
could certainly be *convenient* when the data being processed was
predominantly ASCII text, and the occasional bit of data corruption was
unlikely to be even detected, let alone cause problems, but it's hardly a
solid foundation for building robust multilingual applications (as anyone
that has ever had to track down an errant ``UnicodeError`` in Python 2 will
know).

However, Python 3 does provide a number of mechanisms for relaxing the default
strict checks in order to handle various text processing use cases (in
particular, use cases where "best effort" processing is acceptable, and strict
correctness is not required). This article aims to explain some of them by
looking at cases where it would be appropriate to use them.

Note that many of the features I discuss below are available in Python 2
as well, but you have to explicitly access them via the ``unicode`` type
and the ``codecs`` module. In Python 3, they're part of the behaviour of
the ``str`` type and the ``open`` builtin.


Unicode Basics
--------------

To process text effectively in Python 3, it's necessary to learn at least a
tiny amount about Unicode and text encodings:

1. Python 3 always stores text strings as sequences of Unicode *code points*.
   These are values in the range 0-0x10FFFF. They *don't* always correspond
   directly to the characters you read on your screen, but that distinction
   doesn't matter for most text manipulation tasks.
2. To store text as binary data, you must specify an *encoding* for that text.
3. The process of converting from a sequence of bytes (i.e. binary data)
   to a sequence of code points (i.e. text data) is *decoding*, while the
   reverse process is *encoding*.
4. For historical reasons, the most widely used encoding is ``ascii``, which
   can only handle Unicode code points in the range 0-0x7F (i.e. ASCII is a
   7-bit encoding).
5. There are a wide variety of ASCII *compatible* encodings, which ensure that
   any appearance of a valid ASCII value in the binary data refers to the
   corresponding ASCII character.
6. "utf-8" is becoming the preferred encoding for many applications, as it is
   an ASCII-compatible encoding that can encode any valid Unicode code point.
7. "latin-1" is another significant ASCII-compatible encoding, as it maps byte
   values directly to the first 256 Unicode code points. (Note that Windows
   has it's own "latin-1" variant called cp1252, but, unlike the ISO
   "latin-1" implemented by the Python codec with that name, the Windows
   specific variant doesn't map all 256 possible byte values)
8. There are also many ASCII *incompatible* encodings in widespread use,
   particularly in Asian countries (which had to devise their own solutions before
   the rise of Unicode) and on platforms such as Windows, Java and the .NET CLR,
   where many APIs accept text as UTF-16 encoded data.
9. The ``locale.getpreferredencoding()`` call reports the encoding that Python
   will use by default for most operations that require an encoding (e.g.
   reading in a text file without a specified encoding). This is designed to
   aid interoperability between Python and the host operating system, but can
   cause problems with interoperability between systems (if encoding issues
   are not managed consistently).
10. The ``sys.getfilesystemencoding()`` call reports the encoding that Python
    will use by default for most operations that both require an encoding and
    involve textual metadata in the filesystem (e.g. determining the results
    of ``os.listdir()``)
11. If you're a native English speaker residing in an English speaking country
    (like me!) it's tempting to think "but Python 2 works fine, why are you
    bothering me with all this Unicode malarkey?". It's worth trying to remember
    that we're actually a minority on this planet and, for most people on Earth,
    ASCII and ``latin-1`` can't even handle their *name*, let alone any other
    text they might want to write or process in their native language.


Unicode Error Handlers
----------------------

To help standardise various techniques for dealing with Unicode encoding and
decoding errors, Python includes a concept of Unicode error handlers that
are automatically invoked whenever a problem is encountered in the process
of encoding or decoding text.

I'm not going to cover all of them in this article, but three are of
particular significance:

* ``strict``: this is the default error handler that just raises
  ``UnicodeDecodeError`` for decoding problems and ``UnicodeEncodeError`` for
  encoding problems.
* ``surrogateescape``: this is the error handler that Python uses for most
  OS facing APIs to gracefully cope with encoding problems in the data
  supplied by the OS. It handles decoding errors by squirreling the data away
  in a little used part of the Unicode code point space (For those interested
  in more detail, see `PEP 383`_). When encoding, it translates those hidden
  away values back into the exact original byte sequence that failed to
  decode correctly. Just as this is useful for OS APIs, it can make it easier
  to gracefully handle encoding problems in other contexts.
* ``backslashreplace``: this is an encoding error handler that converts
  code points that can't be represented in the target encoding to the
  equivalent Python string numeric escape sequence. It makes it easy to
  ensure that ``UnicodeEncodeError`` will never be thrown, but doesn't lose
  much information while doing so losing (since we don't want encoding
  problems hiding error output, this error handler is enabled on
  ``sys.stderr`` by default).

.. _PEP 383: http://www.python.org/dev/peps/pep-0383/


The Binary Option
-----------------

One alternative that is always available is to open files in binary mode and
process them as bytes rather than as text. This can work in many cases,
especially those where the ASCII markers are embedded in genuinely arbitrary
binary data.

However, for both "text data with unknown encoding" and "text data with known
encoding, but potentially containing encoding errors", it is often
preferable to get them into a form that can be handled as text strings. In
particular, some APIs that accept both bytes and text may be very strict
about the encoding of the bytes they accept (for example, the
``urllib.urlparse`` module accepts only pure ASCII data for processing as
bytes, but will happily process text strings containing non-ASCII
code points).


Text File Processing
--------------------

This section explores a number of use cases that can arise when processing
text. Text encoding is a sufficiently complex topic that there's no one
size fits all answer - the right answer for a given application will depend
on factors like:

* how much control you have over the text encodings used
* whether avoiding program failure is more important than avoiding data
  corruption or vice-versa
* how common encoding errors are expected to be, and whether they need to
  be handled gracefully or can simply be rejected as invalid input


Files in an ASCII compatible encoding, best effort is acceptable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Use case:** the files to be processed are in an ASCII compatible encoding,
but you don't know exactly which one. *All* files must be processed without
triggering any exceptions, but some risk of data corruption is deemed
acceptable (e.g. collating log files from multiple sources where some
data errors are acceptable, so long as the logs remain largely intact).

**Approach:** use the "latin-1" encoding to map byte values directly to the
first 256 Unicode code points. This is the closest equivalent Python 3
offers to the permissive Python 2 text handling model.

**Example:** ``f = open(fname, encoding="latin-1")``

.. note::

   While the Windows ``cp1252`` encoding is also sometimes referred to as
   "latin-1", it doesn't map all possible byte values, and thus needs
   to be used in combination with the ``surrogateescape`` error handler to
   ensure it never throws ``UnicodeDecodeError``. The ``latin-1`` encoding
   in Python implements ISO_8859-1:1987 which maps all possible byte values
   to the first 256 Unicode code points, and thus ensures decoding errors
   will never occur regardless of the configured error handler.

**Consequences:**

* data will *not* be corrupted if it is simply read in, processed as ASCII
  text, and written back out again.
* will never raise UnicodeDecodeError when reading data
* will still raise UnicodeEncodeError if codepoints above 0xFF (e.g. smart
  quotes copied from a word processing program) are added to the text string
  before it is encoded back to bytes. To prevent such errors, use the
  ``backslashreplace`` error handler (or one of the other error handlers
  that replaces Unicode code points without a representation in the target
  encoding with sequences of ASCII code points).
* data corruption may occur if the source data is in an ASCII incompatible
  encoding (e.g. UTF-16)
* corruption may occur if data is written back out using an encoding other
  than ``latin-1``
* corruption may occur if the non-ASCII elements of the string are modified
  directly (e.g. for a variable width encoding like UTF-8 that has been
  decoded as ``latin-1`` instead, slicing the string at an arbitrary point
  may split a multi-byte character into two pieces)


Files in an ASCII compatible encoding, minimise risk of data corruption
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Use case:** the files to be processed are in an ASCII compatible encoding,
but you don't know exactly which one. *All* files must be processed without
triggering any exceptions, but some Unicode related errors are acceptable in
order to reduce the risk of data corruption (e.g. collating log files from
multiple sources, but wanting more explicit notification when the collated
data is at risk of corruption due to programming errors that violate the
assumption of writing the data back out only in its original encoding)

**Approach:** use the ``ascii`` encoding with the ``surrogateescape`` error
handler.

**Example:** ``f = open(fname, encoding="ascii", errors="surrogateescape")``

**Consequences:**

* data will *not* be corrupted if it is simply read in, processed as ASCII
  text, and written back out again.
* will never raise UnicodeDecodeError when reading data
* will still raise UnicodeEncodeError if codepoints above 0xFF (e.g. smart
  quotes copied from a word processing program) are added to the text string
  before it is encoded back to bytes. To prevent such errors, use the
  ``backslashreplace`` error handler (or one of the other error handlers
  that replaces Unicode code points without a representation in the target
  encoding with sequences of ASCII code points).
* will also raise UnicodeEncodeError if an attempt is made to encode a text
  string containing escaped bytes values without enabling the
  ``surrogateescape`` error handler (or an even more tolerant handler like
  ``backslashreplace``).
* some Unicode processing libraries that ensure a code point sequence is
  valid text may complain about the escaping mechanism used (I'm not going
  to explain what it means here, but the phrase "lone surrogate" is a hint
  that something along those lines may be happening - the fact that
  "surrogate" also appears in the name of the error handler is not a
  coincidence).
* data corruption may still occur if the source data is in an ASCII
  incompatible encoding (e.g. UTF-16)
* data corruption is also still possible if the escaped portions of the
  string are modified directly


Files in a typical platform specific encoding
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Use case:** the files to be processed are in a consistent encoding, the
encoding can be determined from the OS details and locale settings and it
is acceptable to refuse to process files that are not properly encoded.

**Approach:** simply open the file in text mode. This use case describes the
default behaviour in Python 3.

**Example:** ``f = open(fname)``

**Consequences:**

* ``UnicodeDecodeError`` may be thrown when reading such files (if the data is not
  actually in the encoding returned by ``locale.getpreferredencoding()``)
* ``UnicodeEncodeError`` may be thrown when writing such files (if attempting to
  write out code points which have no representation in the target encoding).
* the ``surrogateescape`` error handler can be used to be more tolerant of
  encoding errors if it is necessary to make a best effort attempt to process
  files that contain such errors instead of rejecting them outright as invalid
  input.


Files in a consistent, known encoding
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Use case:** the files to be processed are nominally in a consistent
encoding, you know the exact encoding in advance and it is acceptable to
refuse to process files that are not properly encoded. This is becoming more
and more common, especially with many text file formats beginning to
standardise on UTF-8 as the preferred text encoding.

**Approach:** open the file in text mode with the appropriate encoding

**Example:** ``f = open(fname, encoding="utf-8")``

**Consequences:**

* ``UnicodeDecodeError`` may be thrown when reading such files (if the data is not
  actually in the specified encoding)
* ``UnicodeEncodeError`` may be thrown when writing such files (if attempting to
  write out code points which have no representation in the target encoding).
* the ``surrogateescape`` error handler can be used to be more tolerant of
  encoding errors if it is necessary to make a best effort attempt to process
  files that contain such errors instead of rejecting them outright as invalid
  input.


Files with a reliable encoding marker
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Use case:** the files to be processed include markers that specify the
nominal encoding (with a default encoding assumed if no marker is present)
and it is acceptable to refuse to process files that are not properly encoded.

**Approach:** first open the file in binary mode to look for the encoding
marker, then reopen in text mode with the identified encoding.

**Example:** ``f = tokenize.open(fname)`` uses PEP 263 encoding markers to
detect the encoding of Python source files (defaulting to UTF-8 if no
encoding marker is detected)

**Consequences:**

* can handle files in different encodings
* may still raise UnicodeDecodeError if the encoding marker is incorrect
* must ensure marker is set correctly when writing such files
* even if it is not the default encoding, individual files can still be
  set to use UTF-8 as the encoding in order to support encoding almost
  all Unicode code points
* the ``surrogateescape`` error handler can be used to be more tolerant of
  encoding errors if it is necessary to make a best effort attempt to process
  files that contain such errors instead of rejecting them outright as invalid
  input.
