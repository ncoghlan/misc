Suite Expressions
=================

python-ideas: http://mail.python.org/pipermail/python-ideas/2011-December/013003.html

This idea had an unusual start to life as a "devil's advocate" style response
to a long, rambling trollerific post to python-dev.

It ended up being a reasonably coherent write-up of a "delimited suites for
Python" proposal that didn't make me run screaming in horror, and several
other people had similar reactions, so I decided to include a cleaned up
version of it here.

If anyone does decide to take this idea and run with it, try running ``from
__future__ import braces`` at the interactive prompt to get some idea of how
big a can of worms you're going to be opening (however, also remember that
Guido's views on the topic have `moderated somewhat`_ over the years)

.. _moderated somewhat: http://mail.python.org/pipermail/python-dev/2011-December/114871.html


Background
----------

Python's whitespace based delineation of suites is one of its greatest
strengths. It aligns what the human reader perceives with what the
computer is actually executing, reducing the frequency of semantic
errors due to mismatches between the use of separate block delimiters
and the human readable indentation.

However, this benefit comes at quite a high price: it is effectively
impossible to embed arbitrary Python statements into any environment
where leading whitespace is *not* significant, including Python's own
expression syntax.

It can be argued that this restriction has led directly to the
introduction of "expression friendly" variants of several Python top
level constructs (for example, lambda expressions, conditional
expressions and as a contributing factor in creating the various forms
of comprehension).

It is also one of the reasons Python-based templating languages almost
always create their own custom syntax - embedding Python's own
whitespace sensitive statement syntax into environments where leading
whitespace is either ignored or forms a significant part of the
template output is a formidable challenge.

In other languages, this kind of issue is handled by using explicit
suite and statement delimiters (often braces and semi-colons,
respectively) to allow full suites to be used as expressions.


Rationale
---------

To elaborate on the points made in the Background section, the reason
significant leading whitespace can be problematic is due to two main
circumstances:

1. Attempting to transport it through a channel that either strips
   leading and trailing whitespace from lines, or else consolidates
   certain whitespace sequences into a single whitespace character
   (generally sequences of spaces and tabs becoming a single space).
   Python source code simply cannot be passed through such channels
   correctly - if they don't offer an escaping mechanism, or that
   mechanism is not applied correctly, the code *will* be corrupted.
   Explicitly delimited code, on the other hand, can be passed through
   without semantic alteration (even if the details of the whitespace
   change) and a pretty printer can fix it at the far end.

2. Attempting to transport it through a channel where leading
   whitespace already has another meaning. This comes up primarily with
   templating languages - your whitespace is generally part of the
   template output, so it becomes problematic to break up your Python
   code across multiple code snippets while keeping the suite groupings
   clear. With explicit delimiters, though, you can just ignore the
   template parts, and pretend the code snippets are all part of a single
   string.

A delimited syntax allows definition of a standard way to pass Python source
code through such channels. Since Python expression syntax is one such medium,
this then leads immediately to the possibility of supporting multi-line
lambdas (amongst other things).


Proposal
--------

While Python uses braces for another purpose (dictionary and set
definitions), it is already the case that semi-colons (``;``) can be
used as statement terminators, both optionally at the end of any
simple statement, and also to combine multiple simple statements into
a single larger statement (e.g. ``x += y; print(x)``).

It seems that this existing feature could be combined with a
brace-based notation to create an unambiguous "suite expression"
syntax that would enjoy the same semantics as ordinary Python suites
(i.e. doesn't create a new scope, doesn't directly affect control
flow), but allows *all* Python statements to be embedded inside
expressions.

Currently, the character sequence ``{:`` is a Syntax Error: you are
attempting to end a compound statement header line while an opening
brace remains unmatched, or else trying to build a dictionary without
specifying the key value. This creates an opportunity to re-use braces
for a suite expression syntax without conflicting with their use for
set and dictionary construction.

Specifically, it should be possible to create a variant of the
top-level Python syntax that:

1. Explicitly delimits suites using the notation ``{:`` to open the
   suite and ``:}`` to end it
2. Requires the use of ``;`` to separate simple statements (i.e.
   newline characters would not end a statement, since we would be inside
   an expression)
3. Allows compound statements to be used as simple statements by requiring
   that all subordinate suites also be suite expressions (i.e. leading
   whitespace would not be significant, since we would be using
   subexpressions to define each suite)

This would be sufficient to have a version of Python's syntax that is both
compatible with the existing syntax and could be embedded in
whitespace-insensitive contexts without encountering problems with
suite delineation. However, with one additional change, this new format
could also be used to define "suite expressions" that could be used
meaningfully anywhere Python currently accepts an expression:

4. Uses the value of the last statement executed in the suite as the result
   of the overall suite expression (since return statements would affect the
   containing scope)

This would finally allow the oft-requested "multi-line lambdas", since the
body of the lambda could now be a suite expression.

.. note: Ruby's block notation and C's comma expressions are pretty much
   direct inspiration for the above feature set


Examples
--------

Raise expressions::

    x = y if y is not None else {: raise ValueError("y must not be None!") :}

Try expressions::

    x = {: try {: y.hello} except AttributeError {: "world!"} :}

With expressions::

    data = {: with open(fname) as f {: f.read() :} :}

Embedded assignments::

    if {: m = pat.search(data); m is not None :}:
        # do something with m
    else:
        # No match!

In-order conditional expressions::

    x = {: if a {:b:} else {:c:} :}

One-line accumulator function::

    def acc(n=0): return lambda (i) {: nonlocal n; n += i; n :}

A Python-based templating engine ([1_])::

    <% if danger_level > 3 {: %>

    <div class="alert">
      <% if danger_level == 5 {: %>EXTREME <% :} %>DANGER ALERT!
    </div>

    <% :} elif danger_level > 0 {: %>

    <div>Some chance of danger</div>

    <% :} else {: %>

    <div>No danger</div>

    <% :} %>

    <% for a in ['cat', 'dog', 'rabbit'] {: %>

    <h2><%= a %></h2>
    <p><%= describe_animal(a) %></p>

    <% :} %>

.. [1] Based on an initial example by Simon Baird:
   https://gist.github.com/1455210
