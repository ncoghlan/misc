Python 3 Q & A
==============

Last Updated: 31st December, 2013

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
You can see the full history of changes in the `source repo
<https://bitbucket.org/ncoghlan/misc/history-node/default/notes/python3/questions_and_answers.rst?at=default>`__.

The views expressed below are my own. While many of them are shared by
other core developers, and I use "we" in several places where I believe
that to be the case, I don't claim to be writing on the behalf of every
core developer on every point.

I am also not writing on behalf of the Python Software Foundation (of which
I am a nominated member) nor on behalf of Red Hat (my current employer).
However, I do use several Red Hat specific examples when discussing
enterprise perception and adoption of the Python platform - effectively
bridging that gap between early adopters and the vast majority of prospective
platform users is kinda what Red Hat specialises in, so I consider them an
important measure of the inroads Python 3 is making into more conservative
development communities.

As with all essays on these pages, feedback is welcome via the
`issue tracker`_ or `Twitter`_.

.. _issue tracker: https://bitbucket.org/ncoghlan/misc/issues
.. _Twitter: https://twitter.com/ncoghlan_dev


TL;DR Version
-------------

* Yes, we know this migration is disruptive.
* Yes, we know that some sections of the community have never personally
  experienced the problems with the Python 2 Unicode model that this
  migration is designed to eliminate
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
  where English is not the primary spoken language.

It is my perspective that the web and GUI developers have the right idea:
dealing with Unicode text correctly is not optional in the modern world.
In large part, the Python 3 redesign involved taking Unicode handling
principles elaborated in other parts of the community and building them
into the core design of the language.


Why was Python 3 made incompatible with Python 2?
-------------------------------------------------

To the best of my knowledge, the initial decision to make Python 3
incompatible with the Python 2 series arose from Guido's desire to solve
one core problem: helping *all* Python applications (including the
standard library itself) to handle Unicode text in a more consistent and
reliable fashion without needing to rely on third party libraries and
frameworks. Even if that wasn't Guido's original motivation, it's the
rationale that *I* find most persuasive.

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
Unicode model doesn't follow that guideline: it allows implicit decoding
at almost any point where an 8-bit string encounters a Unicode string, along
with implicit encoding at almost any location where an 8-bit string is
needed but a Unicode string is provided.

The reason this approach is problematic is that it means the traceback for
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

Ned Batchelder's wonderful `Pragmatic Unicode`_ talk/essay could just as
well be titled "This is why Python 3 exists".

Python 3 also embeds Unicode support more deeply into the language itself.
With UTF-8 as the default source encoding (instead of ASCII) and all text
being handled as Unicode, many parts of the language that were previously
restricted to ASCII text (such as identifiers) now permit a much wider range
of Unicode characters. This permits developers with a native language other
than English to use names in their own language rather than being forced to
use names that fit within the ASCII character set.

Removing the implicit type conversions also made it more practical to
implement the new internal Unicode data model for Python 3.3, where
the internal representation of Unicode strings is automatically adjusted
based on the highest value code point that needs to be stored (see
`PEP 393`_ for details).

.. _Misc/unicode.txt: http://svn.python.org/view/python/trunk/Misc/unicode.txt?view=log&pathrev=25264
.. _python-3000 mailing list: http://mail.python.org/pipermail/python-3000/
.. _PEP 393: http://www.python.org/dev/peps/pep-0393/
.. _Pragmatic Unicode: http://nedbatchelder.com/text/unipain.html


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


When can we expect Python 3 to be the obvious choice for new projects?
----------------------------------------------------------------------

Going in to this transition process, my personal estimate was that
it would take roughly 5 years to get from the first production ready release
of Python 3 to the point where its ecosystem would be sufficiently mature for
it to be recommended unreservedly for all *new* Python projects.

Since 3.0 turned out to be a false start due to its IO stack being unusably
slow, I start that counter from the release of 3.1: June 27, 2009.
In the latest update of this Q&A (December 31, 2013), that puts us only
6 months away from that original goal.

In the past few years, key parts of the ecosystem have successfully added
Python 3 support. NumPy and the rest of the scientific Python stack supports
both versions, as do several GUI frameworks (including PyGame). The Pyramid,
Django and Flask web frameworks support both versions, as does the mod_wsgi
Python application server, and the py2exe Windows binary creator. The
upgrade of Pillow from a repackaging project to a full development fork also
brought PIL support to Python 3.

This means that Twisted and gevent are the main critical dependencies that
don't support Python 3 yet, but solid progress has been made in both cases.
In the case of gevent, gevent 1.1 is likely to feature Python 3 compatibility
(there has been a working fork with Python 3 support for several months).
Python 3 support in Twisted may take a while longer to arrive, but *new*
projects have the option of using Guido van Rossum's ``asyncio`` module
instead (this is a new addition to the standard library in Python 3.4, also
`available on PyPI <https://pypi.python.org/pypi/asyncio>`__ for Python 3.3).

There is a `Python 2 or Python 3`_ page on the Python wiki which aims to
provides a reasonably up to date overview of the current state of the
transition.

I think Python 3.3 is a superior language to 2.7 in almost every way (with
the error reporting improvements being the ones I miss most in my day job
working on a Python 2.6 application). There are still several rough edges
in Python 3.3 where certain text and binary data manipulation operations are
less convenient than they are in 2.7, but most of those have been squared
away in 3.4 (there are a couple of remaining issues that should mainly only
affect system admininstators and people writing operating system level
utilities, and only in the presence of improperly encoded data or
misconfigured systems that incorrectly tell Python to use the POSIX locale).

Python 3.4 takes a big step forward in usability for beginners by providing
``pip`` by default, as well as updating the native virtual environment tool
(``pyvenv``) to automatically install pip into new environments. While
trainers in enterprise environments may still wish to teach Python 2 by
default for a few more years, this particular change creates a strong
incentive for community workshops to favour Python 3.4+ after it is
released early in 2014.

Support in enterprise Linux distributions is also a key point for uptake
of Python 3. Canonical have already shipped a supported version (Python 3.2
in Ubuntu 12.04 LTS) with a `stated goal`_ of eliminating Python 2 from the
live install CD for 14.04 LTS. A Python 3 stack has existed in Fedora since
Fedora 13 and has been growing over time, and there is now a stated goal
to remove Python 2 from the live install CDs by the `end of 2014`_
(Fedora 22). Red Hat also now ship a fully supported Python 3.3 runtime as
part of our `Red Hat Software Collections`_ product and the OpenShift
Enterprise self-hosted Platform-as-a-Service offering.

The Arch Linux team have gone even further, making Python 3 the
`default Python`_ on Arch installations. I am `dubious`_ as to the wisdom
of that strategy at this stage of the transition, but I certainly can't
complain about the vote of confidence!

.. _Python 2 or Python 3: http://wiki.python.org/moin/Python2orPython3
.. _stated goal: https://wiki.ubuntu.com/Python
.. _end of 2014: https://fedoraproject.org/wiki/Changes/Python_3_as_Default
.. _Red Hat Software Collections: http://developerblog.redhat.com/2013/09/12/rhscl1-ga/
.. _default Python: https://www.archlinux.org/news/python-is-now-python-3/
.. _dubious: http://www.python.org/dev/peps/pep-0394/


When can we expect Python 2 to be a purely historical relic?
------------------------------------------------------------

Python 2 is still a good language. While I think Python 3 is a *better*
language (especially when it comes to error reporting), we've deliberately
designed the migration plan so users can update on *their* timetable rather
than ours, and we expect commercial redistributors to extend that timeline
even further.

I personally expect Python 2.7 to remain a reasonably common development
platform for at least another decade (that is, until 2023). The recent
public beta of Red Hat Enterprise Linux 7 uses Python 2.7 as the system
Python, and many library, framework and application developers base their
minimum supported version of Python on the system Python in RHEL (especially
since that also becomes the system Python in downstream rebuilds like CentOS
and Scientific Linux).


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
*obviously* "Python 2". Right now (December 2013), the answer is "either is
a reasonable choice, although context may favour Python 2". With the release
of Python 3.4 next year, the obvious answer *should* become "Python 3.4,
unless you have a compelling reason to choose Python 2 instead". Possible
compelling reasons include "I am teaching the course to maintainers of an
existing Python 2 code base", "We have a large in-house collection of
existing Python 2 only support libraries we want to reuse" and "I only use
the version of Python provided by my Linux distro vendor and they currently
only support Python 2" (although that last is also changing on the *vendor*
side - Red Hat now supports Python 3.3 through both Red Hat Software
Collections and as part of OpenShift Enterprise, and Canonical have
supported Python 3.2 since 12.04 LTS).

Note the question that *isn't* on the list: "I have a large Python 2
application which is working well for me. Should I migrate it to Python 3?".

We're happy enough for the answer to *that* question to remain "No"
indefinitely. While it is likely that platform effects will eventually shift
even the answer to that question to "Yes" (and Python 2 will have a much
nicer exit strategy to a newer language than COBOL ever did), the time
frame for *that* change is a lot longer than the five years that was
projected for changing the default choice of Python version for green field
projects.

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
* developers complaining that the core development team isn't being
  aggressive enough in forcing the community to migrate promptly rather than
  allowing the migration to proceed at its own pace (!)

That last case is a new one, and the difference in perspective appears to
be an instance of the classic early adopter/early majority divide in
platform adoption. The deliberately gentle migration plan is for the
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

For the inverse question relating to the concern that the existing migration
plan is too *aggressive*, see :ref:`abandoning-users`.


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
support for Python 3.2, 3.3, and the upcoming 3.4 release. With the
``codecs`` and ``email`` modules being brought into line, the upcoming
Python 3.4 release is the first one where the transition feels close to
being "done" to me in terms of coping with the full implications of a
strictly enforced distinction between binary and text data in the standard
library. However, I still expect that feedback process will continue
throughout the 3.x series, since "mostly done" and "done" are very different
things.

In addition to the cases where blurring the binary/text distinction really
did make things simpler in Python 2, we're also forcing even developers in
strict ASCII-only environments to have to care about Unicode correctness,
or else explicitly tell the interpreter not to worry about it. This means
that Python 2 users that may have previously been able to ignore Unicode
issues may need to account for them properly when migrating to Python 3.

I've written more extensively on both of these topics in
:ref:`binary-protocols` and :ref:`py3k-text-files`.


Why is Python 3 considered a better language to teach beginning programmers?
----------------------------------------------------------------------------

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

Python 2 is still a good language despite these flaws, but users that are
happy with Python 2 shouldn't labour under the misapprehension that the
language is perfect. We have made mistakes, and Python 3 came about because
Guido and the rest of the core development team finally became tired of
making excuses for those limitations, and decided to start down the long
road towards fixing them instead.

All of the above issues have been  addressed by backwards incompatible
changes in Python 3. Once we had made that decision, then adding other
new features *twice* (once to Python 3 and again to Python 2) imposed
significant additional development effort, although we *did* do so for a
number of years (the Python 2.6 and 2.7 releases were both developed in
parallel with Python 3 releases, and include many changes originally created
for Python 3 that were backported to Python 2 since they were backwards
compatible and didn't rely on other Python 3 only changes like the new,
more Unicode friendly, IO stack).

I'll give several examples below of how the above behaviours have changed in
Python 3.3 (since that's the currently released version), as well as
mentioning other improvements coming up in Python 3.4.

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

Python 3 has learned how to do basic arithmetic, and only has one kind of
integer::

    >>> 3 / 4
    0.75
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
the handler has finished running). The networking security changes are
intermixed with the IO stack changes for Unicode support, so backporting
those, while technically possible, would be a non-trivial task.

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
the code runs correctly under both versions.

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
will be supported until at least 2023. On Windows and Mac OS X, commercial
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

If that happens, then I expect we'll accept it as true evidence of demand for
a 2.8 release, and I'll be the first to make the case for us adopting such a
fork and making it official. I personally doubt that will happen though, as
such a release wouldn't achieve all that much that isn't already possible
through ``pip`` and PyPI, would be incredibly time consuming, and would be
highly unlikely to be seen as providing a good return on investment for
potential corporate sponsors.

So far, we haven't even seen a concerted effort to create a community
"Python 2.7+" release that bundles all of the available 3.x backport
libraries with the base 2.7 distribution (which would be a much simpler
project), so the prospects for a successful Python 2.8 fork that actually
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
statement to prove.

A third alternative that would make us seriously question our current
strategy is if community workshops aimed at new programmers chose not to
switch to recommending Python 3.4 by default after it is released, *despite*
the significant carrots of ``pip`` being provided by default on Windows and
Mac OS X and integrated into ``pyvenv`` on all platforms, the inclusion
of :mod:`pathlib`, :mod:`statistics`, :mod:`asyncio`, more secure default
settings for SSL/TLS, `etc <http://docs.python.org/3.4/whatsnew/3.4.html>`__.


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
the Stackless team are `currently looking at
<http://stackless.com/pipermail/stackless/2013-November/005934.html>`__
taking is to consistently use the name "Stackless 2.8" and avoid referring
to the new variant as a different version of Python.


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
* Fork Python 2 to add the missing features for their own benefit
* Migrate to a language other than Python

The first three of those approaches are all fully supported by python-dev.
Many standard library additions in Python 3 started as modules on PyPI and
thus remain available to Python 2 users. For other cases, such as ``unittest``
or ``configparser``, the respective standard library maintainer also maintains
a PyPI backport.

The latter two choices are unfortunate, but we've done what we can to make
the first three alternatives more attractive.

.. _quite emphatic: http://www.python.org/dev/peps/pep-0404/


Doesn't this make Python look like an immature and unstable platform?
---------------------------------------------------------------------

Again, many of us in core development are aware of this concern, and
have been taking active steps to ensure that even the most risk averse
enterprise users can feel comfortable in adopting Python for their
development stack, despite the current transition.

Obviously, much of the content in the previous two questions regarding the
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

Some notable changes within the Python 3 series, specifically PEP 3333 (which
updated the Web Server Gateway Interface to cope with the Python 3 text
model) and PEP 414 (which restored support for explicit Unicode literals)
have been driven primarily by the expressed needs of the web development
community in order to make Python 3 better meet their needs.

If you want to keep track of Python's development and get some idea of
what's coming down the pipe in the future, it's all
`available on the internet`_.

.. _available on the internet: http://docs.python.org/devguide/communication.html


But, but, surely fixing the GIL is more important than fixing Unicode...
------------------------------------------------------------------------

While this complaint isn't really Python 3 specific, it comes up often
enough that I wanted to put in writing why most of the core development
team simply don't see the GIL as a particularly big problem in practice.

Earlier versions of this section were needlessly dismissive of the
concerns of those that wish to combine their preference for programming
in Python with their preference for using threads to exploit the
capabilities of multiple cores on a single machine. In the interests of
clear communication, the text has been rewritten in a more constructive
tone. If you wish to see the snarkier early versions, they're
available in the `source repo`_ for this site.

.. _source repo: https://bitbucket.org/ncoghlan/misc

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
capable hardware becomes more common.

As far as a free-threaded CPython implementation goes, that seems unlikely
in the absence of a corporate sponsor willing to pay for the development and
maintenance of the necessary high performance cross-platform threading
primitives, their incorporation into a fork of CPython, and the extensive
testing needed to ensure compatibility with the existing CPython ecosystem,
and then persuading python-dev to accept the additional maintenance burden
imposed by accepting such changes back into the reference implementation.

I personally expect most potential corporate sponsors with a vested interest
in Python to spend their money more cost effectively and just tell their
engineers to use multiple processes instead of threads, or else to
contribute to sponsoring Armin's work on `Software Transactional Memory`_.

.. _Software Transactional Memory: http://morepypy.blogspot.com.au/2011/08/we-need-software-transactional-memory.html
.. _further tweaks: http://bugs.python.org/issue7946
.. _pickle protocol: http://www.python.org/dev/peps/pep-3154/
.. _Trent Nelson's work: http://vimeo.com/79539317
