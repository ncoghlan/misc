PEP Ideas: Free to a good home
==============================

My ability to generate ideas for ways in which Python could potentially be
improved in various areas vastly outstrips the time I'm willing to spend
following up on them, kicking them around with other community members and
turning them into suggestions that may actually prove to be a genuine
enhancement to the language rather than just useless cruft new Python
programmers have to learn in order to understand code other programmers might
write.

To help keep myself vaguely sane, I'm currently limiting myself to pushing
`PEP 380`_ through to completion (adding the ``yield from`` syntax to Python
3.3, along with some `associated updates`_ to the :mod:`dis` module to make our
own testing easier), exploring a few miscellaneous enhancements to shell
scripting functionality (my `walkdir`_ and `shell_command`_ PyPI packages),
making the main module a better behaved member of the Python import system
(through `PEP 395`_) and helping to finalise our official recommendation to
Linux distros on managing the Python 2 to Python 3 transition (via `PEP 394`_).

Those are just the highlights, too - there's plenty of other tracker,
python-dev and python-ideas traffic relating to proposals others are working
on, and various smaller fixes in my areas of interest, as well as a few longer
term projects relating to better encapsulating the import state and updating
the compiler to better leverage the AST for a variety of purposes.

.. _associated updates: http://bugs.python.org/issue11816
.. _PEP 380: http://www.python.org/dev/peps/pep-0380/
.. _PEP 394: http://www.python.org/dev/peps/pep-0394/
.. _PEP 395: http://www.python.org/dev/peps/pep-0395/
.. _walkdir: http://walkdir.readthedocs.com
.. _shell_command: http://shell-command.readthedocs.com

What that means is that there are plenty of ideas I've had that may actually
have some merit, but that I don't have the time to explore. Be aware that
some of these are going to be *bad* ideas that justifiably won't survive the
gauntlet of python-ideas and python-dev review, while others may make sense
as esoteric PyPI modules rather than as standard library or core language
additions.

.. note: Several of these articles are just placeholders for the moment. In
   those cases, they have a link to relevant python-ideas posts or past blog
   posts. Explore a little - these are generally things I've written a fair
   bit about in the past.

.. toctree::
   :maxdepth: 2

   strview.rst
   suite_expr.rst
   implicit_with.rst
   skip_with.rst
   ast_metaprogramming.rst
   preview_namespace.rst

