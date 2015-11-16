# Python Packaging:<br/>Today and<br/>Tomorrow

---

# What is</br>software distribution?

# Presenter Notes

* getting software from the people that wrote it to people that would
  benefit from using it
* changed radically by the internet
* software distribution is now an expected language feature

----

# Developers:<br/>Cross platform<br/>tools are great!

# Presenter Notes

* Same commands on any Linux distro and even Mac OS X and Windows

----

# Integrators:<br/>Language specific<br/>tools are awful!

# Presenter Notes

* C, C++, Java, Python, Perl, Ruby, Javascript, Haskell
* Erlang, Rust, Go, ...
* New distribution tools --> new security vulnerabilities
* Auditing and certification still matter

----

# What does this mean for Python?

# Presenter Notes

* distribution tools historically Linux centric
* assumed a C/C++ development background
* both of those assumptions are now outdated
* many folks learning programming through Python on Windows
* challenging community assumptions is hard work!

---

# Empowering<br/>distutils-sig

# Presenter Notes

* CPython core dev is focused on the next iteration of Python
* packaging updates need to support all widely deployed versions
* the current baseline is Python 2.6 (mostly due to RHEL & CentOS 6)
* PEP process changed to delegate more authority to distutils-sig
* python-dev now only involved when actually changing CPython
* aligns communities with the work that needs to be done

---

# The Python<br/>Packaging<br/>Authority

# Presenter Notes

* creators of pip and virtualenv, popular third party tools
* now the home of the core projects in the Python packaging ecosystem
* each project still has its own ways of making design decisions
* interoperability is managed through the PEP process

---

# Bundling the pip<br/>package manager<br/>(PEP 453, PEP 477)

# Presenter Notes

* Python 3.4 (released in March) shipped with pip pre-installed
* Python 2.7.9 (due in December) will bundle pip on Windows and Mac OS X
* Have worked with Debian, Ubuntu & Fedora devs to figure out the Linux side
* Allows for much easier bootstrapping of everything else

---

# Handling<br/>security<br/>concerns

# Presenter Notes

* PyPI is still an uncurated index - no warranties given or implied
* Language level tooling aims to ensure user downloads what dev uploaded
* Currently bundle a copy of the Mozilla cert database
* One goal of the standard library SSL enhancements is to let us eventually
  stop doing that and use the system cert database instead

---

# Bundling virtual<br/>environments<br/>(PEP 405)

# Presenter Notes

* Cooperative isolation of Python level application dependencies
* Provided by default in Python 3.3, but not as useful without pip
* Installs pip by default in 3.4
* Fully integrated with core interpreter
* "pip install virtualenv" still works and is consistent across versions

---

# Binary package<br/>support<br/>(PEP 427)

# Presenter Notes

* Binary egg format has been around for a decade
* Had various issues that significantly limited its adoption
* The newer wheel format addressed most of those concerns
* Now supported on PyPI for Mac OS X and Windows
* Can be used with a private index for any platform

----

# Standardised<br/>versioning scheme<br/>(PEP 440)

# Presenter Notes

* Strict versioning syntax restrictions and ordering rules
    * Eliminates the need to guess
    * Covers almost all projects currently on PyPI
    * Includes various features to better support redistributors
* Semantic versioning for dependencies by default, other options like
  prefix matching allowed
* Local version identifiers allow redistributors to indicate exact patch
  level, while still satisfying version specifiers

---

# packaging.python.org

# Presenter Notes

* now the home of an agreed set of guidelines for Python packaging
* already linked from Python 3 docs now that pip is bundled
* will be linked from Python 2 docs once Python 2.7.9 is released

---

# conda:<br/>a cross-platform<br/>platform

# Presenter Notes

* all the preceding tools work within an existing Python runtime
* can't be used to manage Python runtimes themselves
* also have trouble dealing with the FORTRAN dependencies of the Scientific
  Python stack
* conda trades reduced integration with the OS for greater cross platform
  consistency
* not a PyPA project (since it isn't Python specific), but an option to
  consider if you're looking for an open source cross platform dependency
  management system designed with the needs of Pythonistas in mind

----

# Where are we<br/>going next?

# Presenter Notes

* work to date provides parity with most language specific ecosystems
* next step is to aim to move significantly beyond them

----

# Python packaging<br/>metadata 2.0<br/>(PEP 426)

# Presenter Notes

* Complex data model for a complex problem
* JSON compatible in memory data representation
* Suitable for use in both APIs and as a serialisation format
* Generated metadata, focused on *tool* interoperability
* Up to tool developers to decide how to expose it to users
* `setuptools` will continue to use `setup.py`
* Can be distributed in *parallel* with existing metadata formats
* Far more opinionated about valid metadata contents (but still compatible
  with almost all existing PyPI projects)

----

# Designed for redistribution

# Presenter Notes

* Actually includes the notion of system integrators and
  redistributors in the upstream data model
* Aim is to allow distros to work *with* the upstream packaging
  system, rather than having it fight them every step of the
  way
* Strongly discourage version pinning when publishing
  software - design for security updates

----

# Dependencies:<br/>run & meta<br/>build, test & dev

# Presenter Notes

* Currently splits dependencies into 5 categories: run, meta, build, test, dev
* `run_requires`: runtime dependencies
* `meta_requires`: redistribution of exact versions of other components
* `build_requires`: build dependencies
* `test_requires`: test suite execution dependencies
* `dev_requires`: other tools needed by project developers

----

# Standard metadata extensions

# Presenter Notes

* Extension mechanism to record arbitrary settings in the metadata
* Standard extensions cover optional info that is useful, but not
  essential for declaring and installing dependencies
* Allows for separate contact info for the upstream project and the
  integrator in redistributed versions
* Packages can declare extensions "mandatory" so installers that don't
  understand the extension will refuse to install them

----

# Binary packages<br/>for Linux<br/>(wheel 2.0?)

# Presenter Notes

* All Linux distros currently get the same wheel compatibility tags
* Nothing comparable to the python.org binary builds to anchor ABI
  compatibility
* That's why Linux wheels aren't allowed on PyPI
* Main near term idea being considered is to allow some mechanism for
  overriding the standard compatibility tags
* Longer term, may add a compatibility field based on /etc/os-release

----

# End to end<br/>package signing<br/>(PEP 458)

# Presenter Notes

* Current security model relies heavily on TLS
* Means we can't run a public mirror network
* Using a CDN donated by Fastly
* Proposal to use "The Update Framework" for end to end signing
* Seems like a reasonable idea, but currently working on hardening other
  aspects of the PyPI infrastructure

----

# Q & A<br/><br/>@ncoghlan_dev
