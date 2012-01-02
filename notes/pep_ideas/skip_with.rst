Skipping the With Statement Body
================================

Boredom & Laziness: http://www.boredomandlaziness.org/2011/01/some-goals-for-python-33.html

(Note: I'm no longer a fan of this idea. `contextlib2.ContextStack`_ should
provide a way to achive the same thing programmatically in ``__enter__``
without needing to change the context management protocol)

Basic concept is to add an optional ``__entered__`` method to the context
management protocol that gets executed *inside* the scope of the try block,
so any exceptions it raises are seen by the context managers ``__exit__``
method.

.. _contextlib2.ContextStack: https://bitbucket.org/ncoghlan/contextlib2/issue/2/add-recipes-and-more-examples-for
