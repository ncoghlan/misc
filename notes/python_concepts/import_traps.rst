Traps for the Unwary in Python's Import System
==============================================

Python's import system is powerful, but also quite complicated. Until the
release of Python 3.3, there was no comprehensive explanation of the expected
import semantics, and even following the release of 3.3, the details of how
``sys.path`` is initialised are still somewhat challenging to figure out.

Even though 3.3 cleaned up a lot of things, it still has to deal with
various backwards compatibility issues that can cause strange behaviour,
and may need to be understood in order to figure out how some third party
frameworks operate.

Furthermore, even without invoking any of the more exotic features of the
import system, there are quite a few common missteps that come up regularly
on mailing lists and Q&A sites like Stack Overflow.

This essay only officially covers Python versions back to Python 2.6. Much
of it applies to earlier versions as well, but I won't be qualifying any of
the explanations with version details before 2.6.

As with all my essays on this site, suggestions for improvement or
requests for clarification can be posted on BitBucket_.

.. _BitBucket: https://bitbucket.org/ncoghlan/misc/issues


The missing __init__.py trap
----------------------------

This particular trap applies to 2.x releases, as well as 3.x releases up to
and including 3.2.

Prior to Python 3.3, filesystem directories, and directories within zipfiles,
*had* to contain an ``__init__.py`` in order to be recognised as Python
package directories. Even if there is no initialisation code to run when
the package is imported, an empty ``__init__.py`` file is still needed for
the interpreter to find any modules or subpackages in that directory.

This has changed in Python 3.3: now any directory on ``sys.path`` with a name
that matches the package name being looked for will be recognised as
contributing modules and subpackages to that package.

Consider this directory layout::

    project/
        example/
            foo.py

Where ``foo.py`` contains the source code::

    print("Hello from ", __name__)

With that layout and the current working directory being ``project``, Python 2.7 gives the
following behaviour::

    $ python2 -c "import example.foo"
    Traceback (most recent call last):
      File "<string>", line 1, in <module>
    ImportError: No module named example.foo

While Python 3.3+ is able to import the submodule without any problems::

    $ python3 -c "import example.foo"
    Hello from  example.foo

The __init__.py trap
--------------------

This is an all new trap added in Python 3.3 as a consequence of fixing the
previous trap: if a subdirectory encountered on ``sys.path`` as part of
a package import contains an ``__init__.py`` file, then the Python
interpreter will create a *single directory* package containing only
modules from that directory, rather than finding all appropriately
named subdirectories as described in the previous section.

This happens *even if* there are other preceding subdirectories on
``sys.path`` that match the desired package name, but do not include an
``__init__.py`` file.

Let's take the preceding layout, and add a second project that *also* has
an ``example`` directory, but includes an ``__init__.py`` file in it,
as well as a ``bar.py`` file with the same contents as ``foo.py``::

    project/
        example/
            foo.py
    project2/
        example/
            __init__.py
            bar.py

If we explicitly add the second project to ``PYTHONPATH``, we find that
Python 3.3+ can't find ``example.foo`` either, as the directory containing
``__init__.py`` file prevents the creation of a multi-directory namespace
package::

    $ PYTHONPATH=../project2 python3 -c "import example.bar"
    Hello from  example.bar
    $ PYTHONPATH=../project2 python3 -c "import example.foo"
    Traceback (most recent call last):
      File "<string>", line 1, in <module>
    ImportError: No module named 'example.foo'

However, if we remove the offending ``__init__.py`` file, Python 3.3+ will
automatically create a namespace package and be able to see both submodules::

    $ rm ../project2/example/__init__.py 
    $ PYTHONPATH=../project2 python3 -c "import example.bar"
    Hello from  example.bar
    $ PYTHONPATH=../project2 python3 -c "import example.foo"
    Hello from  example.foo

This complexity is primarily forced on us by backwards compatibility
constraints - without it, some existing code would have broken when Python
3.3 made the presence of ``__init__.py`` files in packages optional.

However, it is also useful in that it makes it possible to explicitly
declare that a package is closed to additional contributions. All of
the standard library currently works that way, although some packages
may open up their namespaces to third party contributions in future
releases (the key challenge with that idea is that namespace packages
can't offer any package level functionality, which creates a major
backwards compatibility problem for existing standard library packages).


The double import trap
----------------------

This next trap exists in all current versions of Python, including 3.3, and
can be summed up in the following general guideline: "Never add a package
directory, or any directory inside a package, directly to the Python path".

The reason this is problematic is that every module in that directory is
now potentially accessible under two different names: as a top level module
(since the directory is on ``sys.path``) and as a submodule of the
package (if the higher level directory containing the package itself is
also on ``sys.path``).

As an example, Django (up to and including version 1.3) used to be guilty of setting
up exactly this situation for site-specific applications - the application
ends up being accessible as both ``app`` and ``site.app`` in the module
namespace, and these are actually two *different* copies of the module. This
is a recipe for confusion if there is any meaningful mutable module level
state, so this behaviour was eliminated from the default project layout
in version 1.4 (site-specific apps now always need to be fully qualified
with the site name, as described in the `release notes`_).

.. _release notes: https://docs.djangoproject.com/en/dev/releases/1.4/#updated-default-project-layout-and-manage-py

Unfortunately, this is still a *really* easy guideline to violate, as it
happens automatically if you attempt to run a module inside a package from
the command line by filename rather than using the ``-m`` switch.

Consider a project & package layout like the following (I typically use package
layouts along these lines in my own projects - a lot of people hate nesting
tests inside package directories like this, and prefer a parallel hierarchy,
but I favour the ability to use explicit relative imports to keep module
tests independent of the package name)::

    project/
        setup.py
        example/
            __init__.py
            foo.py
            tests/
                __init__.py
                test_foo.py

What's surprising about this layout is that all of the following
ways to invoke ``test_foo.py`` *probably won't work* due to broken imports
(either failing to find ``example`` for absolute imports like
``import example.foo`` or ``from example import foo``, complaining about
relative imports in a non-package or beyond the top-level package for
explicit relative imports like ``from .. import foo``, or issuing even more
obscure errors if some other submodule happens to shadow the name of a
top-level module used by the test, such as an ``example.json`` module
that handled serialisation or an ``example.tests.unittest`` test runner)::

    # These commands will most likely *FAIL* due to problems with the way
    # the import state gets initialised, even if the test code is correct

    # working directory: project/example/tests
    ./test_foo.py
    python test_foo.py
    python -m test_foo
    python -c "from test_foo import main; main()"

    # working directory: project/example
    tests/test_foo.py
    python tests/test_foo.py
    python -m tests.test_foo
    python -c "from tests.test_foo import main; main()"

    # working directory: project
    example/tests/test_foo.py
    python example/tests/test_foo.py

    # working directory: project/..
    project/example/tests/test_foo.py
    python project/example/tests/test_foo.py
    python -m project.example.tests.test_foo
    python -c "from project.example.tests.test_foo import main; main()"

That's right, that long list is of all the methods of invocation that are
quite likely to *break* if you try them, and the error messages won't make
any sense if you're not already intimately familiar not only with the way
Python's import system works, but also with how it gets initialised. (Note
that if the project exclusively uses explicit relative imports for
intra-package references, the last two commands shown may actually work
for Python 3.3 and later versions. Any absolute imports that expect
"example" to be a top level package will still break though).

For a long time, the only way to get ``sys.path`` right with this kind of
setup was to either set it manually in ``test_foo.py`` itself (hardly
something novice, or even many veteran, Python programmers are going to
know how to do) or else to make sure to import the module instead of
executing it directly::

    # working directory: project
    python -c "from example.tests.test_foo import main; main()"

Since Python 2.6, however, the following also works properly::

    # working directory: project
    python -m example.tests.test_foo

This last approach is actually how I prefer to use my shell when
programming in Python - leave my working directory set to the project
directory, and then use the ``-m`` switch to execute relevant submodules
like tests or command line tools. If I need to work in a different
directory for some reason, well, that's why I also like to have multiple
shell sessions open.

While I'm using an embedded test case as an example here, similar issues
arise any time you execute a script directly from inside a package without
using the ``-m`` switch from the parent directory in order to ensure that
``sys.path`` is initialised correctly (e.g. the pre-1.4 Django project
layout gets into trouble by running ``manage.py`` from inside a package,
which puts the package directory on ``sys.path`` and leads to this double
import problem - the 1.4+ layout solves that by moving ``manage.py`` outside
the package directory).

The fact that most methods of invoking Python code from the command line
break when that code is inside a package, and the two that do work are highly
sensitive to the current working directory is all thoroughly confusing for a
beginner. I personally believe it is one of the key factors leading
to the perception that Python packages are complicated and hard to get right.

This problem isn't even limited to the command line - if ``test_foo.py`` is
open in Idle and you attempt to run it by pressing F5, or if you try to run
it by clicking on it in a graphical filebrowser, then it will fail in just
the same way it would if run directly from the command line.

There's a reason the general "no package directories on ``sys.path``"
guideline exists, and the fact that the interpreter itself doesn't follow
it when determining ``sys.path[0]`` is the root cause of all sorts of grief.

However, even if there are improvements in this area in future versions of
Python, this trap will still exist in all current versions.


Executing the main module twice
-------------------------------

This is a variant of the above double import problem that doesn't require any
erroneous ``sys.path`` entries.

It's specific to the situation where the main module is *also* imported as
an ordinary module, effectively creating two instances of the same module
under different names.

As with any double-import problem, if the state stored in ``__main__`` is
significant to the correct operation of the program, or if there is
top-level code in the main module that has undesirable side effects if
executed more than once, then this duplication can cause obscure and
surprising errors.

This is just one more reason why main modules in more complex applications
should be kept fairly minimal - it's generally far more robust to move most
of the functionality to a function or object in a separate module, and just
import that module from the main module. That way, inadvertently executing
the main module twice becomes harmless. Keeping main modules small and
simple also helps to avoid a few potential problems with object
serialisation as well as with the multiprocessing package.


The name shadowing trap
-----------------------

Another common trap, especially for beginners, is using a local module name
that shadows the name of a standard library or third party package or module
that the application relies on. One particularly surprising way to run afoul
of this trap is by using such a name for a *script*, as this then combines
with the previous "executing the main module twice" trap to cause trouble.
For example, if experimenting to learn more about Python's :mod:`socket`
module, you may be inclined to call your experimental script ``socket.py``.
It turns out this is a really bad idea, as using such a name means the
Python interpreter can no longer find the *real* socket module in the
standard library, as the apparent socket module in the current directory
gets in the way::

    $ python -c 'from socket import socket; print("OK!")'
    OK!
    $ echo 'from socket import socket; print("OK!")' > socket.py
    $ python socket.py
    Traceback (most recent call last):
      File "socket.py", line 1, in <module>
        from socket import socket
      File "/home/ncoghlan/devel/socket.py", line 1, in <module>
        from socket import socket
    ImportError: cannot import name socket


The stale bytecode file trap
----------------------------

Following on from the example in the previous section, suppose we decide to
fix our poor choice of script name by renaming the file. In Python 2, we'll
find that still doesn't work::

    $ mv socket.py socket_play.py
    $ python socket_play.py
    Traceback (most recent call last):
      File "socket_play.py", line 1, in <module>
        from socket import socket
      File "/home/ncoghlan/devel/socket.py", line 1, in <module>
        # Wrapper module for _socket, providing some additional facilities
    ImportError: cannot import name socket

There's clearly something strange going on here, as we're seeing a traceback
that claims to be caused by a *comment* line. In reality, what has happened
is that the cached bytecode file from our previous failed import attempt is
still present and causing trouble, but when Python tries to display the
source line for the traceback, it finds the source line from the standard
library module instead. Removing the stale bytecode file makes things work as
expected::

    $ rm socket.pyc
    $ python socket_play.py
    OK!

This particular trap has been largely eliminated in Python 3.2 and later. In
those versions, the interpreter makes a distinction between standalone
bytecode files (such as ``socket.pyc`` above) and cached bytecode files
(stored in automatically created ``__pycache__`` directories). The latter
will be ignored by the interpreter if the corresponding source file is
missing, so the above renaming of the source file works as intended::

    $ echo 'from socket import socket; print("OK!")' > socket.py
    $ python3 socket.py
    Traceback (most recent call last):
      File "socket.py", line 1, in <module>
        from socket import socket
      File "/home/ncoghlan/devel/socket.py", line 1, in <module>
        from socket import socket
    ImportError: cannot import name socket
    $ mv socket.py socket_play.py
    $ python3 socket_play.py

Note, however, that mixing Python 2 and Python 3 can cause trouble if
Python 2 has left a standalone bytecode file lying around::

    $ python3 socket_play.py
    Traceback (most recent call last):
      File "socket_play.py", line 1, in <module>
        from socket import socket; print("OK!")
    ImportError: Bad magic number in /home/ncoghlan/devel/socket.pyc

If you're not a core developer on a Python implementation, the problem of
importing stale bytecode is most likely to arise when renaming Python source
files. For Python implementation developers, it can also arise any time
we're working on the compiler components that are responsible for
generating the bytecode in the first place - that's the main reason
the CPython ``Makefile`` includes a ``make pycremoval`` target.

The submodules are added to the package namespace trap
------------------------------------------------------

Many users will have experienced the issue of trying to use a submodule
when only importing the package that it is in::

    $ python3
    >>> import logging
    >>> logging.config
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AttributeError: 'module' object has no attribute 'config'
    
But it is less common knowledge that when a submodule is loaded *anywhere*
it is automatically added to the global namespace of the package::

    $ echo "import logging.config" > weirdimport.py
    $ python3
    >>> import weirdimport
    >>> import logging
    >>> logging.config
    <module 'logging.config' from '/usr/local/Cellar/python3/3.4.3/Frameworks/Python.framework/Versions/3.4/lib/python3.4/logging/config.py'>
    
This is most likely to surprise you when in an ``__init__.py`` and you are
importing or defining a value that has the same name as a submodule of the
current package. If the submodule is loaded by *any* module at any point
after the import or definition of the same name, it will shadow the
imported or defined name in the ``__init__.py``'s global namespace.

More exotic traps
-----------------

The above are the common traps, but there are others, especially if you
start getting into the business of extending or overriding the default
import system.

I may add more details on each of these over time:

* the weird signature of ``__import__``
* the influence of the module globals (``__import__``, ``__path__``,
  ``__package__``)
* `issues with threads`_ prior to 3.3
* the lack of PEP 302 support in the default machinery prior to 3.3
* non-cooperative package portions in pre-3.3 namespace packages
* sys.path[0] initialisation variations
* more on the issues with pickle, multiprocessing and the main module
  (see PEP 395)
* ``__main__`` is not always a top level module (thanks to ``-m``)
* the fact modules are allowed to replace themselves in sys.modules
  during import
* ``__file__`` may not refer to a real filesystem location
* since 3.2, you can't just add ``c`` or ``o`` to get the cached bytecode
  filename

.. _issues with threads: http://docs.python.org/2/library/threading#importing-in-threaded-code
