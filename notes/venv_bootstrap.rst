Bootstrapping a Python Virtual Environment
==========================================

I'm working on an application that eventually needs to be deployed to an
environment that runs Python 2.6. My local development environment is Fedora
16 and runs Python 2.7 as the system Python.

While I could work in a full virtual machine where the system Python is 2.6,
that would be needlessly painful (since it would be a lot more isolated than I
really need, isolating all my development tool settings along with the Python
runtime). Instead, I'd like to be able to develop for 2.6 as easily as I can
for 2.7, *without* running any risk of breaking my system Python installation.

Accordingly, since Fedora only ships the one Python stack, I needed to
bootstrap a full 2.6 virtual environment to get my development environment
to better reflect the intended deployment environment.

Initially I assumed that the various packaging tools would allow virtual
environments for other Python versions to be managed just using the system
Python installation. I still believe that's actually the case (at least
for the two virtual environment specific tools). In practice, however, I
found it to be something of a pain to get that working properly, so I went
down the path of isolating the virtual environment implementation as well.
This approach also has the added virtue of still working even if the affected
tools *aren't* installed for the system Python installation.

These instructions won't work on Windows. If a Windows enthusiast decides
to write up how to do this in the extra-special Microsoft way, I'll be happy
to provide a link to it.

These instructions *should* work on Mac OS X and on any *nix system. Let me
know if they don't and I'll either fix them or note any platform specific
idiosyncrasies.

These instructions also won't work for any Python version prior to 2.6. They
rely on the "Per user site-packages directory" feature introduced by PEP 370,
and that feature was first included in 2.6.


Step 1: Python 2.6
------------------

Since there's no prebuilt version of Python 2.6 in the Fedora repos, the
easiest solution for me was to just build my own copy from source::

    # This first step can be quite slow. It was quick for me, since
    # I could copy one of my existing local clones of the repo
    $ hg clone http://hg.python.org/cpython python26
    $ cd python26
    $ hg update 2.6
    $ ./configure
    $ make
    $ sudo make altinstall

.. warning:
   Be *very* sure to type ``altinstall`` in that final line. Doing a full
   install (which overwrites the system Python) could make for a very bad
   day, especially on systems that rely on a working Python installation
   to run their software update tools (e.g. any ``yum`` based distro).

And we now have a ``python2.6`` available on the system path. This is also
the only ``sudo`` invocation we're going to use, since the rest of the
bootstrap process involves downloading and running a whole pile of unverified
code. Accordingly, for everything else, we'll install it into the user's
home directory to limit the damage we can do.

(You could possibly find a way to avoid even this use of ``sudo``, but
there's also a reasonable chance at least one of the Python package
management tools would get confused. It's more reliable to just run with
an installed version of Python).

If you're not in the habit of building Python from source, then the
instructions on `getting set up`_ in the CPython developer guide may
be useful. Just do a ``hg update`` to the appropriate branch before
running ``./configure`` and drop the ``--with-pydebug`` flag (as shown
above). Don't worry if some of the optional extension modules fail to
build (unless you specifically need those modules - then you'll have
to do the research on what additional development packages are
needed on your system in order to build them).

.. _getting set up: http://docs.python.org/devguide/setup.html

Specifically using a source build isn't essential here - the important
point is getting access to an installed binary for the appropriate version
of Python. It just so happens that, for me, a source build is the easiest
way to achieve that end.


Step 2: ``distribute``
----------------------

The installation instructions for ``pip``,  ``virtualenv`` and ``distribute``
are full of annoying circular references, since none of them can be sure
what system state you're starting from. They're all basically fine if you
can use a pre-packaged version of ``pip`` or are using the system Python
installation, but if you're trying to build up an independent Python stack
from nothing it can be hard to figure out where to start.

The appropriate starting point is actually ``distribute``, since both of the
others need it to work (technically you can also use the older ``setuptools``.
However, ``distribute`` is the better choice, for a variety of complicated
reasons that I'm not going to go into here).

Alas, the bootstrap script mentioned in the ``distribute`` installation
documentation currently only works for installing into the system package
directory, so we need to do the installation dance manually (check PyPI
for the latest version of ``distribute`` before following these
instructions, don't just blindly copy and paste these commands)::

    $ curl -O http://pypi.python.org/packages/source/d/distribute/distribute-0.6.24.tar.gz
    $ tar -xzvf distribute-0.6.24.tar.gz
    $ cd distribute-0.6.24
    $ python2.6 setup.py install --user

There's two important differences to note here relative to the normal
instructions in the ``distribute`` documentation:

1. We've specifically called ``python2.6`` rather than just ``python``
2. We've passed the ``--user`` flag so it is installed just for us

Starting with the next release, the bootstrap script will support ``--user``
as well, so the above instructions can be simplified to::

    $ curl -O http://python-distribute.org/distribute_setup.py
    $ python2.6 distribute_setup.py --user


Step 3: ``pip``
---------------

We want to be able to install packages globally within our alternative Python
stack, as well as within virtual environments, so an independent installation
of ``pip`` is our next task.

Once again, the bootstrap script only works for a system installation, so
we'll be doing another tarball installation:

    $ curl -O http://pypi.python.org/packages/source/p/pip/pip-1.0.2.tar.gz
    $ tar -xzvf pip-1.0.2.tar.gz
    $ cd pip-1.0.2
    $ python2.6 setup.py install --user

As with ``distribute``, we've adjusted the final command so it installs into
our private user directory for the Python 2.6 stack.

Since we're going to want to actually *run* the main ``pip`` script, though,
we'll create a couple of convenient shell aliases for it::

    $ alias pip26="~/.local/bin/pip-2.6"
    $ alias install26="pip26 install --user"


Step 4: Virtual Environments
----------------------------

We've made it through the clumsiest parts now - with ``pip`` available, we
can use it to get version appropriate copies of other libraries from PyPI.

The first two we're going to grab are ``virtualenv`` and
``virtualenvwrapper``, so we don't have to rely on them being installed
in the system Python::

    $ install26 virtualenv
    $ install26 virtualenvwrapper

These two allow us to maintain separate dependency stacks for various
projects, making it easy to generate dependency specifications when it
comes time to package them for deployment. It also allows us to work
switch between projects with conflicting dependencies with lower
workflow overheads than completely separate virtual machines.

Now, these two projects assume you're going to be using the system Python
installation to manage virtual environments, even those for other Python
versions. We're not going to do that though, so we create version specific
copies of the relevant scripts::

    $ cp ~/.local/bin/virtualenv ~/.local/bin/virtualenv-2.6
    $ cp ~/.local/bin/virtualenvwrapper.sh ~/.local/bin/virtualenvwrapper-2.6.sh


There are also some settings we need to configure to ensure that ``pip``
automatically respects active virtual environments when installing
packages, as well as to avoid conflicting with any virtual environments
associated with the system Python installation (or any other Python
installations in parallel with this one).

Accordingly, we'll also add a few lines to our shell profile
(e.g. ``~/.bashrc``) to make sure these features are appropriately
configured whenever we log in (if you plan to regularly switch between
the system Python and your custom Python for development, you'll likely
want to skip this part, put it in a separate shell script you can load
when needed, or figure out how to reliably manage the virtual environments
for other versions using the system Python's ``virtualenv`` and
``virtualenvwrapper`` installations)::

    # Set up virtualenvwrapper to use our just installed Python binary
    # and our personal copies of virtualenv and distribute
    export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python2.6
    export VIRTUALENVWRAPPER_VIRTUALENV=~/.local/bin/virtualenv-2.6
    export VIRTUALENVWRAPPER_VIRTUALENV_ARGS='--no-site-packages --distribute'
    export WORKON_HOME=~/.virtualenvs26
    source ~/.local/bin/virtualenvwrapper-2.6.sh
    # Set up our pip convenience shortcuts
    alias pip26="~/.local/bin/pip-2.6"
    alias install26="pip26 install --user"
    # Set pip to play nicely with our virtual environments by default
    export PIP_VIRTUALENV_BASE=$WORKON_HOME
    export PIP_RESPECT_VIRTUALENV=true

Because we're working on a custom Python installation with nothing
installed in ``site-packages``, the above configuration leaves site
package processing enabled by default in virtual environments. This
allows us to use ``install26 module`` to install a module and have
it visible to all of our virtual environments.

The ``source`` command makes it easy to rerun the shell initialisation
code (specify the appropriate file for your own system)::

    $ source ~/.bashrc


Step 5: Working on Projects
---------------------------

Starting a new virtual environment with ``virtualenvwrapper`` is just a
matter of running::

    $ mkvirtualenv envname

From this point, the modules you install will be based on the dependencies
of the specific project you're working on. If there are packages you
*always* need, you may choose to install them directly into your user
package directory. Otherwise, you may install them into specific virtual
environments.

For example, since I want to use the new Python 2.7 ``unittest`` features in
Python 2.6, I'm going to need to install the ``unittest2`` backport module::

    $ install26 unittest2

That command will install it into my user packages directory, so it will be
visible from all my virtual environments (that don't have site-package
processing disabled). Alternatively, since ``pip`` has been configured to
play nicely with virtual environments, the following command will install
``unittest2`` solely into the current environment::

    $ pip26 install unittest2

That's barely scratching the surface of what these tools allow you to do,
since this guide is just about getting an environment up and running that
makes it *easy* to grab packages from PyPI during development in a way
that is unlikely to compromise your entire development system
("Look Ma, no sudo!").

Consult the documentation of the various projects mentioned for more
details on the full scope of the features they provide:

* distribute: http://packages.python.org/distribute/
* pip: http://www.pip-installer.org
* virtualenv: http://pypi.python.org/pypi/virtualenv
* virtualenvwrapper: http://www.doughellmann.com/docs/virtualenvwrapper/

