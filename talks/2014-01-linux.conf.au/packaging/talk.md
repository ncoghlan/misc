# Python Packaging 2.0:<br/>Playing Well With Others

----

## <br/>Nick Coghlan (@ncoghlan_dev)

* CPython core developer since 2005
* Nominated member of the PSF
* Red Hat toolsmith
* "BDFL Delegate" for Python packaging

----

# Python packaging is `______`?

# Presenter Notes

* The newcomer's lament
* "Why is Python packaging so bad?"
* They're not wrong
* Especially compared to more modern tools like npm (Node.js)
* Something needed to change

----

# Critical social issues

# Presenter Notes

* Traditionally laissez faire attitude from PyPI coordinators
* Effective change requires more opinionated policies and guidance
* Effective change also requires consensus and a transition plan
* Modest change proposals imposed pain without significant gain
* How could we finally say "Yes!" to more ambitious proposals?

----

# PEP process changes

# Presenter Notes

* PEPs are Python Enhancement Proposals
* Historically, python-dev got to comment directly on *all* PEPs
* This is a problem when expertise is concentrated elsewhere
* Changed in 2013 to allow other groups to use the PEP process directly
* Places more emphasis on the Discussions-To header in the PEP
* Requires an active BDFL Delegate on the nominated list
* Core language and standard library PEPs must still go to python-dev

----

# What is a<br/>BDFL Delegate?

# Presenter Notes

* The Python core development team's solution to "Guido doesn't scale"
* Guido van Rossum is Python's Benevolent Dictator for Life
* Historically, all Python Enhancement Proposals required BDFL approval
* This doesn't work well for problems that Guido finds uninteresting
* "BDFL Delegates" are people Guido trusts to approve PEPs on his behalf
* See PEP 1 for the details of how it works in practice

----

# Enter the Python Packaging Authority

# Presenter Notes

* Adopted an "ecosystem first" model (rather than "standard library first")
* Empowered distutils-sig to discuss and approve packaging related PEPs
* BDFL Delegates: me (in general) & Richard Jones (PyPI in particular)
* Already resulted in a substantial shift in the mood of distutils-sig
    * Previously: "Everything is broken and there's nothing we can do"
    * Now: "Many things are still broken, but we're working on that"

----

# Near term improvements

# Presenter Notes

* Primary aim: eliminate "setup.py install" on production systems
* Shipping pip 1.5 with Python 3.4 (Fedora Python 3 maintainer is working on a
  distro friendly redesign of the bundling mechanism)
* Referencing PyPA's cross-version guide from the version specific docs
* Adopting the wheel format for distribution of pre-built binaries on
  Windows and Mac OS X, and build caching on POSIX systems
* Reimplementing PyPI as a modern web application with decent automated
  testing (https://preview-pypi.python.org)
* PEP 458 covers using the Update Framework for end-to-end security, but
  we need to upgrade PyPI before that will be practical to implement

----

# Next step:<br/>Play well with others

# Presenter Notes

* There are some other technical issues with the current packaging ecosystem
* A couple of those are Python specific
* Our current scheme predates JSON, so its an eclectic mix of ad hoc formats
* Must download full distributions to read metadata
* But there's a more general problem I don't think *anyone* has solved yet...

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

# Integrating with<br/>Linux distributions

# Presenter Notes

* I got involved after having to repackage PyPI projects as RPMs
* Currently lots of manual tweaks needed to get RPM spec files right,
  because the metadata is either missing upstream, or isn't in a usable
  form
* I believe it's possible to make this not horrible, but both the distros
  and upstream need to be involved in order to make it work

----

# PEP 426:<br/>Packaging metadata 2.0

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

# Designing for redistribution

# Presenter Notes

* Actually includes the notion of system integrators and
  redistributors in the upstream data model
* Aim is to allow distro to work *with* the upstream packaging
  system, rather than having it fight them every step of the
  way
* Strongly discourage version pinning when publishing
  software - design for security updates

----

# Updating versioning system

# Presenter Notes

* Strict versioning syntax restrictions and ordering rules
    * Eliminates the need to guess
    * Covers almost all projects currently on PyPI
    * Includes "build labels" to help projects with incompatible schemes
    * Includes an "integrator suffix" to allow integrators to indicate
      rebuilds and patches, while still satisfying version specifiers
* Semantic versioning for dependencies by default, other options like
  prefix matching allowed
* Can opt in to exact matches, but PyPI will complain if you do
* Integrator suffixes will be ignored for version matching

----

# Dependencies:<br/>run & meta<br/>build, test & dev

# Presenter Notes

* Splits dependencies into 5 categories: run, meta, build, test, dev
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
* Details are still very much in flux, but the metadata hook system should
  allow the binary wheel format to cover all "setup.py install" use cases
  that are not yet handled

----

# Work in progress

# Presenter Notes

* Background discussion while we work on the near term improvements
* Exact scope of 2.0 isn't yet nailed down, but at this point removing
  things is more likely than adding more
* Would love feedback from more distro packaging folks as to whether or
  not this is likely to help with streamlining the repackaging
  process
* better support for declaring FHS compliant destinations on POSIX systems
  is on the todo list but may not make 2.0 (and is technically part of
  the wheel spec anyway)
* increased build system flexibility is also on the todo list
* allowing system wide dependencies to be automatically satisfied through
  the system package manager wherever possible (with a warning to use
  virtual environments or per-user installations otherwise)

----

# Q & A

* Metadata PEPs:
    * http://www.python.org/dev/peps/pep-0426/
    * http://www.python.org/dev/peps/pep-0440/
    * http://www.python.org/dev/peps/pep-0459/
* distutils-sig mailing list:
    * http://mail.python.org/mailman/listinfo/distutils-sig
