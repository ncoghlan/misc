Implicit Context Managers
=========================

Boredom & Laziness: http://www.boredomandlaziness.org/2011/01/some-goals-for-python-33.html

Basic concept is to add an optional ``__cm__`` method that relates to context
managers the way ``__iter__`` relates to iterators.

I still don't have a pithy name like "iterable" for "objects with an implicit
context manager", but the passage of time has at least cemented "context
manager" as referring specifically to objects with ``__enter__`` and
``__exit__`` methods.
