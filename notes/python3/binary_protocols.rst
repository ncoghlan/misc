.. _binary-protocols:

Python 3 and ASCII Compatible Binary Protocols
==============================================

Last Updated: 6th January, 2014

If you pay any attention to the Twittersphere (and likely several other
environments), you may have noticed various web framework developers having a
few choice words regarding the Unicode handling design in Python 3.

They actually have good reason to be upset with python-dev: we broke their
world. Not only did we break it, but we did it on purpose.


What did we break?
------------------

What we broke is a very specific thing: many of the previously idiomatic
techniques for transparently accepting both Unicode text and text in an ASCII
compatible binary encoding no longer work in Python 3. Given that the web
(along with network protocols in general) is *built* on the concept of ASCII
compatible binary encodings, this is causing web framework developers an
understandable amount of grief as they start making their first serious efforts
at supporting Python 3.

The key thing that changed is that it is no longer easy to write text
manipulation algorithms that can work transparently on either actual text
(i.e. 2.x ``unicode`` objects) and on text encoded to binary using an ASCII
compatible encoding (i.e. some instances of 2.x ``str`` objects).

There are a few essential changes in Python 3 which make this no longer
practical:

* In 2.x, when ``unicode`` and ``str`` meet, the latter is automatically
  promoted to ``unicode`` (usually assuming a default ``ascii`` encoding). In
  3.x, this changes such that when ``str`` (now always Unicode text) meets
  ``bytes`` (the new binary data type) you get an exception. Significantly,
  this means you can no longer share literal values between the two
  algorithm variants (in 2.x, you could just use ``str`` literals and rely on
  the automatic promotion to cover the ``unicode`` case).
* Iterating over a string produces a series of length 1 strings. Iterating over
  a 3.x bytes object, on the other hand, produces a series of integers.
  Similarly, indexing a bytes object produces an integer - you need to use
  slicing syntax if you want a length 1 bytes object.
* The ``encode()`` and ``decode()`` convenience methods no longer support the
  text->text and binary->binary transforms, instead being limited to the actual
  text->binary and binary->text encodings. The ``codecs.encode`` and
  ``codecs.decode`` functions need to be used instead in order to handle these
  transforms in addition to the regular text encodings (these functions are
  available as far back as Python 2.4, so they're usable in the common subset
  of Python 2 and Python 3).
* In 2.x, the ``unicode`` type supported the buffer API, allowing direct access
  to the raw multi-byte characters (stored as UCS4 in wide builds, and a
  UCS2/UTF-16 hybrid in narrow builds). In 3.x, the only way to access this
  data directly is via the Python C API. At the Python level, you only have
  access to the code point data, not the individual bytes.

The recommended approach to handling both binary and text inputs to an API
without duplicating code is to explicitly decode any binary data on input
and encode it again on output, using one of two options:

1. ``ascii`` in ``strict`` mode (for true 7-bit ASCII data)
2. ``ascii`` in ``surrogateescape`` mode (to allow any ASCII compatible
   encoding)

However, it's important to be very careful with the latter approach - when
applied to an ASCII incompatible encoding, manipulations that assume ASCII
compatibility may still cause data corruption, even with explicit decoding
and encoding steps. It can be better to assume strict ASCII-only data for
implicit conversions, and require external conversion to Unicode for other
ASCII compatible encodings (e.g. this is the approach now taken by the
``urllib.urlparse`` module).


Why did we break it?
--------------------

That last paragraph in the previous section hints at the answer: *assuming*
that binary data uses an ASCII compatible encoding and manipulating it
accordingly can lead to silent data corruption if the assumption is incorrect.

In a world where there are multiple ASCII *incompatible* text encodings in
regular use (e.g. UTF-16, UTF-32, ShiftJIS, many of the CJK codecs), that's
a problem.

Another regular problem with code that supposedly supports both Unicode and
encoded text is that it may not correctly handle multi-byte, variable
width and other stateful encodings where the meaning of the current byte
may depend on the values of one or more previous bytes, even if the code
does happen to correctly handle ASCII-incompatible stateless single-byte
encodings.

All of these problem can be dealt with if you appropriately vet the encoding
of any binary data that is passed in. However,  this is not only often easier
said than done, but Python 2 doesn't really offer you any good tools for
finding out when you've stuffed it up. They're data driven bugs, but the
errors may never turn into exceptions, instead just causing flaws in the
resulting text output.

This was a gross violation of "The Zen of Python", specifically the part about
"Errors should never pass silently. Unless explicitly silenced".

As a concrete example of the kind of obscure errors this can cause, I recently
tracked down an obscure problem that was leading to my web server receiving
a request that consisted solely of the letter "G". From what I have been able
to determine, that error was the result of:

1. M2Crypto emitting a Unicode value for a HTTP header value
2. The SSL connection combining this with other values, creating an entire
   Unicode string instead of the expected byte sequence
3. The SSL connection interpreting that string via the buffer API
4. The SSL connection seeing the additional NULs due to the UCS4 internal
   encoding and truncating the string accordingly

This has now been worked around by explicitly encoding the Unicode value
erroneously emitted, but it was a long hunt to find the problem when the
initial symptom was just a 404 error from the web server.

Since Python 3 is a lot fussier when it comes to the ways it will
allow binary and text data to implicitly interact, this would have been
picked up client side as soon as any attempt was made to combine the
Unicode text value with the already encoded binary data.

The other key reason for changing the text model of the language is that
the Python 2 model only works properly on POSIX systems. Unlike POSIX,
Unicode capable interfaces on Windows, the JVM and the CLR (whether .NET
or mono), use Unicode natively rather than using encoded bytestrings.

The Python 3 model, by contrast, aims to handle Unicode correctly on all
platforms, with the surrogateescape error handler introduced to handle the
case of data in operating system interfaces that doesn't match the declared
encoding on POSIX systems.


Why are the web framework developers irritated?
-----------------------------------------------

We knew when we released Python 3 that it was going to take quite a while for
the binary/text split to be fully resolved. Most of the burden of that
resolution falls on the shoulders of those dealing with the boundaries
between text data and binary protocols. Web frameworks have to deal with
these issues both on the network side *and* on the data storage side.

Those developers also have good reason to want to avoid decoding to Unicode -
until Python 3.3 was released, Unicode strings consumed up to four times
the memory consumed by 8 bit strings (depending on build options).

That means framework developers face an awkward choice in their near term
Python 3 porting efforts:

* do it "right" (i.e. converting to the text format for text manipulations),
  and keep track of the need to convert the result back to bytes
* split their code into parallel binary and text APIs (potentially duplicating
  a lot of code and making it much harder to maintain)
* including multiple "binary or text" checks within the algorithm
  implementation (this can get very untidy very quickly)
* develop a custom extension type for implementing a str-style API on top of
  encoded binary data (this is hard to do without reintroducing all the
  problems with ASCII incompatible encodings noted above, but a custom
  type provides more scope to make it clear it is only appropriate in
  contexts where ASCII compatible encodings can be safely assummed, such
  as many web protocols)

I have a personal preference for the first choice as the current path
of least resistance, as reflected in the way I implemented the binary
input support for the ``urllib.parse`` APIs in Python 3.2. However, the
last option (or something along those lines) will likely be needed in
order to make ASCII compatible binary protocol handling as convenient
in Python 3 as it is in Python 2.

The last option is still one of the options for possible future Python 3
improvements listed under :ref:`room-for-improvement`.


Couldn't the implicit decoding just be disabled in Python 2?
------------------------------------------------------------

While Python 2 *does* provide a mechanism that allows the implicit
decoding mechanism to be disabled, actually trying to use it breaks the
world::

    >>> import urlparse
    >>> urlparse.urlsplit("http://example.com")
    SplitResult(scheme='http', netloc='example.com', path='', query='', fragment='')
    >>> urlparse.urlsplit(u"http://example.com")
    SplitResult(scheme=u'http', netloc=u'example.com', path=u'', query='', fragment='')
    >>> import sys
    >>> reload(sys).setdefaultencoding("undefined")
    >>> urlparse.clear_cache()
    >>> urlparse.urlsplit("http://example.com")
    SplitResult(scheme='http', netloc='example.com', path='', query='', fragment='')
    >>> urlparse.urlsplit(u"http://example.com")
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/usr/lib64/python2.7/urlparse.py", line 181, in urlsplit
        i = url.find(':')
      File "/usr/lib64/python2.7/encodings/undefined.py", line 22, in decode
        raise UnicodeError("undefined encoding")
    UnicodeError: undefined encoding

(If you don't clear the parsing cache after disabling the default encoding
and retest with the same URLs, that second call may appear to be work,
but that's only because it gets a hit in the cache from the earlier
successful call. Using a different URL or clearing the caches as shown
will reveal the error).

This is why turning off the implicit decoding is such a big deal that it
required a major version bump for the language definition: there is
a *lot* of Python 2 code that only handles Unicode because 8-bit strings
(including literals) are implicitly promoted to Unicode as needed. Since
Python 3 removes all the implicit conversions, code that previously relied
on it in order to accept both binary and text inputs (like the Python 2 URL
parsing code shown above) instead needs to be updated to explicitly handle
both binary and text inputs.

So, in contrast to Python 2 code above, the Python 3 version not only
changes the types of the components in the result, but also changes the
type of the result itself::

    >>> from urllib import parse
    >>> parse.urlsplit("http://example.com")
    SplitResult(scheme='http', netloc='example.com', path='', query='', fragment='')
    >>> parse.urlsplit(b"http://example.com")
    SplitResultBytes(scheme=b'http', netloc=b'example.com', path=b'', query=b'', fragment=b'')

However, it's also no longer dependent on a global configuration setting that
controls how 8-bit string literals are converted to Unicode text - instead,
the decision on how to convert from bytes to text is handled entirely
within the function call.


Where to from here?
-------------------

The revised text handling design in Python 3 is definitely a case of the
pursuit of correctness triumphing over convenience. "Usually handy, but
occasionally completely and totally wrong" is not a good way to design a
language (If you question this, compare and contrast the experience of
programming in C++ and Python. Both are languages with a strong C influence,
but the former makes a habit of indulging in premature optimisations that can
go seriously wrong if their assumptions are violated. Guess which of the two
is almost universally seen as being more developer hostile?).

The challenge for Python 3.3 and beyond is to start bringing back some of
the past convenience that resulted from being able to blur the lines between
binary and text data without unduly compromising on the gains in correctness.

The efficient Unicode representation in Python 3.3 (which uses the
smallest per-character size out of 1, 2 and 4 that can handle all characters
in the string) was a solid start down that road, as was the restoration of
Unicode string literal support in :pep:`414` (as that was a change library
and framework developers couldn't address on behalf of their users).

Python 3.4 restored full support for the binary transform codecs through
the existing type neutral codecs module API (along with improved handling
of codec errors in general).

Some other possible steps towards making Python 3 as convenient a langauge
as Python 2 for wire protocol handling are discussed in
:ref:`room-for-improvement`

But for most Python programmers, this issue simply doesn't arise. Binary
data is binary data, text characters are text characters, and the two only
meet at well-defined boundaries. It's only people that are writing the
libraries and frameworks that *implement* those boundaries that really need
to grapple with the details of these concepts.
