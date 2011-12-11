Skipping the With Statement Body
================================

Boredom & Laziness: http://www.boredomandlaziness.org/2011/01/some-goals-for-python-33.html

Basic concept is to add an optional ``__entered__`` method to the context
management protocol that gets executed *inside* the scope of the try block,
so any exceptions it raises are seen by the context managers ``__exit__``
method.