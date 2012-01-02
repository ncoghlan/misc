Skipping the With Statement Body
================================

Boredom & Laziness: http://www.boredomandlaziness.org/2011/01/some-goals-for-python-33.html

(Note: I'm no longer a fan of this idea. `contextlib2.ContextStack`_ should
provide a way to achieve some of the same benefits programmatically in
``__enter__`` without needing to change the context management protocol, at
least as far as resource cleanup goes. It should also make it easier to
create context managers that can be combined with an if statement to only
execute if the resource is acquired successfully)

Basic concept is to add an optional ``__entered__`` method to the context
management protocol that gets executed *inside* the scope of the try block,
so any exceptions it raises are seen by the context managers ``__exit__``
method.

.. _contextlib2.ContextStack: https://bitbucket.org/ncoghlan/contextlib2/issue/2/add-recipes-and-more-examples-for
