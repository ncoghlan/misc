# Nobody Expects the Python Packaging Authority

----

# Who am I?

## Nick Coghlan (@ncoghlan_dev)

* CPython core developer since 2005
* Nominated member of the Python Software Foundation
* Red Hat toolsmith
* Current "BDFL Delegate" for packaging related PEPs

----

# Disclaimer

* This is an early draft of this presentation
* PEP 426 is still in draft and may change before acceptance
* I still have some fact checking to do before PyCon AU
* Still some walls o' text that need to be edited down
* Not yet edited for length (let me know which bits are less interesting!)
* Last year, BrisPy feedback resulted in some major revisions :)

----

# The state of Python packaging

* Standard library: "Distribution is a platform problem"
    * `distutils` is primarily a build system
    * Distribution and installation support is rudimentary at best
    * Expects to be used in conjunction with platform-specific binary
      distribution systems (such as APT, RPM or MSI).
* `setuptools`: "Distribution is a language problem"
    * Improved distribution and installation for `distutils`
    * Doesn't integrate well with platform-specific distribution systems
    * Lots of implicit behaviour, which leads to arcane failure modes
* `pip` and `virtualenv`: "Separate the application from the platform"
    * Using virtual environments avoids most `setuptools` quirks
    * Reduces interference with platform-specific distribution systems
    * `distutils` heritage still results in significant limitations

----

# The beginner's lament

* "Why is Python packaging so complicated/hard/bad?"
* Compared to more modern tools like `npm` (from Node.js) the Python
  software distribution ecosystem is clunky and confusing
* When trying to fix it, it helps to understand the problem!
* Spoilers:
    * Bootstrapping issues (especially on Windows)
    * Lack of clear authoritative documentation
    * Compilation issues for source distributions (especially on Windows)
    * Challenges of cross-platform binary distribution
    * Challenges of integrating with platform specific package managers

----

# The foundations of Python packaging

* First CPython `distutils` commit: [December 1998](http://hg.python.org/cpython-fullhistory/rev/917357c12552)
* PEP 241 (metadata 1.0): March 2001
* First `PyPI` commit: [November 2002](https://bitbucket.org/pypa/pypi/commits/9d6b859b38c838e520fda73f0b2807958ccb1dca)
* PEP 314 (metadata 1.1): April 2003
* First `setuptools` commit: [March 2004](https://bitbucket.org/pypa/setuptools/commits/a5f40bcf16c57d50c1d2bdb891bef1df7bb5af59)

----

# A fundamental social issue

* Traditionally laissez faire attitude from PyPI coordinators
* Effective change requires more opinionated policies and guidance
* Effective change also requires consensus and a transition plan
* Modest change proposals imposed pain without significant gain
* How can we finally say "Yes!" to more ambitious proposals?

----

# PEP process changes

* Historically, python-dev got to comment directly on *all* PEPs
* This is a problem when expertise is concentrated elsewhere
* Changed this year to allow other groups to use the PEP process directly
* Places more emphasis on the Discussions-To header in the PEP
* Requires an active BDFL Delegate on the nominated list
* Core language and standard library PEPs must still go to python-dev

----

# What is a BDFL Delegate?

* The core development team's solution to "Guido doesn't scale"
* Guido van Rossum is Python's Benevolent Dictator for Life
* Historically, all Python Enhancement Proposals required BDFL approval
* This doesn't work well for problems that Guido finds uninteresting
* "BDFL Delegates" are people Guido trusts to approve PEPs on his behalf
* See PEP 1 for the details of how it works in practice

----

# What does this mean for packaging?

* Adopting an "ecosystem first" model (rather than "standard library first")
* Empowered distutils-sig to discuss and approve packaging related PEPs
* Consolidated distutils-sig and catalog-sig
* BDFL Delegates:
    * Packaging in general: Nick Coghlan
    * Python Package Index in particular: Richard Jones
* Already resulted in a substantial shift in the mood of distutils-sig
    * Previously: "Everything is broken and there's nothing we can do"
    * Now: "Many things are still broken, but we're working on that"

----

# Enter the Python Packaging Authority

* Name originally chosen by the creators of `pip` and `virtualenv`
* `virtualenv` inspired the `venv` infrastructure in Python 3.3 (PEP 405)
* `pip` will likely be bootstrapped in Python 3.4 (PEP 439)
* Adopting the PyPA as the home for other core packaging related projects:
    * `setuptools` (post-merger between `setuptools` and `distribute`)
    * `pypi` (source for pypi.python.org)
    * `distlib` (support library derived from `distutils2`)
    * `pylauncher` (Windows Python launcher bundled with Python 3.3+)
* Creating an authoritative guide to Python packaging
    * Currently at https://python-packaging-user-guide.readthedocs.org
    * Will add references from http://docs.python.org once it stabilises
    * Current best guess: after the release of pip 1.4

----

# Distributing the workload

* Coordinators of the current near term changes:
    * Daniel Holth (creator of the 'wheel' format and library, PEP 426 co-author)
    * Donald Stufft (current main PyPI developer, PEP 426 co-author)
    * Marcus Smith (pip lead developer, lead author of the new packaging guide)
    * Jason R. Coombs (post-merger setuptools lead developer, pre-merger distribute lead developer)
    * Noah Kantrowitz (python.org/PSF infrastructure lead)

----

# Distributing the workload (continued)

* Other key contributors:
    * Tarek Ziadé (created distribute and distutils2, wrote PEPs 345, 376 & 386)
    * Phillip J. Eby (created setuptools, coordinated recent distribute reintegration)
    * Éric Araujo (recent distutils2 lead)
    * Vinay Sajip (distlib lead)
    * "The Fellowship of the Packaging" (distribute and distutils2 contributors)
    * Martin von Löwis, Jim Fulton, Holger Krekel, Christian Theune,
      Carl Meyer, Jannis Leidel and others on distutils-sig

----

# Where to from here?

* Two parallel activities
    * Improve the current system (based on setuptools defined metadata)
    * Define a new metadata standard for parallel distribution
* Quickly addresses the worst issues affecting the current ecosystem
* Longer term goal to advance the state of the art

----

# PyPI improvements

* PSF verified by StartSSL and acquired a High Assurance SSL cert
* Forced SSL by default for browser based PyPI interactions
* `setuptools`, `pip` and other tools being updated to use verified SSL
* Docs hosting moved out to a separate *.pythonhosted.org domain
* PEP 438 has started migration away from scraping of external links
    * http://pypi-externals.caremad.io/
* PyPI is now behind a CDN (donated by Fastly)
* Whole of *.python.org will switch to forced SSL once preview.python.org
  becomes the main site (technical limitations currently keep us from
  doing that)

----

# `pip` improvements

* Switching to verified SSL by default (v1.4)
* Adopting the `wheel` format (PEP 427) to support build caching and binary
  distribution (v1.4)
* New option to turn off link spidering (part of PEP 438) (v1.4)
* Migrating core components from `setuptools` to `distlib` (v1.5?)

----

# `setuptools` improvements

* `distribute` merged back into `setuptools 0.7`
* Switching to verified SSL by default (v1.4)
* Can publish `wheel` files (in addition to or instead of eggs) with the
  aid of the Daniel Holth's `wheel` project

----

# A new metadata standard

* There are some fundamental issues with the current packaging ecosystem
* The current packaging ecosystem also has a huge installed base
* Downloading full distributions just to check metadata is insane
* `distutils2` included some excellent ideas, but lacked a transition plan
----

# Three key technical issues

* Eclectic mix of ad hoc formats: why not use JSON?
* Must download full distributions to read metadata
* "Improvements" tend to break the world (for a subset of users)

----

# The trouble with JSON

* `distutils` and PyPI both predate JSON
* json.org: 2002
* simplejson: [December 2005](https://github.com/simplejson/simplejson/commit/5aa76448ef5a7a4cb53540c58c5cf42a04e0a4b2)
* RFC 4627: July 2006
* JSON Schema: June 2010 (first draft)
* PEP 426 (Metadata 2.0) will include a JSON schema definition :)

----

# The trouble with PyPI

* Web Server-Gateway Interface (PEP 333): December 2003
* Django: July 2005
* Flask: May 2010
* Pyramid: January 2011 (June 2008 as repoze.bfg)
* Low-cost CDNs: November 2008 (launch of Amazon CloudFront)
* PyPI 2.0 will be a PostgreSQL backed Django application based on the
  data model defined in PEP 426

----

# The trouble with testing

* Creation of JUnit: 1997
* Agile manifesto: [2001](http://agilemanifesto.org/)
* First CPython `unittest`` commit: [March 2001](http://hg.python.org/cpython-fullhistory/rev/33f7769a218e)
* Interacting tools result in a large number of possible combinations
* A key reason why packaging ecosystem changes tend to break things :(
* New ecosystem components generally have much improved test coverage

----

# Other packaging ecosystems

* Perl's CPAN (and the PAUSE upload service)
* PHP's PEAR and composer
* Ruby's gems and bundler
* Node.js's npm
* RPM and yum
* APT

----

# Challenging design goals

* Integrate cleanly with Linux platform specific package managers
* Support native platform compilers (notably Visual Studio on Windows)
* Account for PyPI's historically laissez faire attitude
* Support older versions of Python (at least as far back as Python 2.6)
* Make it secure by default (ignoring systemic SSL vulnerabilities for now)

----

# Key observations and conclusions

* Properly separate the concerns of publication and integration
* Index servers should be opinionated on behalf of installers
* You need structured metadata (whether one file or multiple)
* If an index server can derive metadata directly from the source code,
  don't ask publication tools to provide it separately
* Cross platform extension building is harder than cross-platform distribution

----

# PEP 426: Packaging metadata 2.0

* Complex data model for a complex problem
* JSON compatible in memory data representation
* Suitable for use in both APIs and as a serialisation format
* Generated metadata, focused on *tool* interoperability
* Up to tool developers to decide how to expose it to users
* `setuptools` will continue to use `setup.py`

----

# PEP 426: General concepts

* Can be distributed in *parallel* with existing metadata
* Far more opinionated about valid metadata contents (but still compatible
  with > 98.7% of existing PyPI projects)
* Semantic dependency model to help automate integration with platform
  package managers
* Retain `setup.py` commands as the build system (at least for now)
* Based on concepts in PEP 345 (metadata 1.2) and setuptools, but with
  additional enhancements and clarifications to help encourage broader
  adoption


----

# PEP 426: Inherited from PEP 345

* Strict versioning syntax restrictions
  * Eliminates the need to guess
  * Compatibility tweaks in 2.0
  * Added "source labels" to help projects with incompatible schemes
* Rich version specifier system
* Environment markers for conditional dependencies
* Separate versioning specification (PEP 440 replaces PEP 386)

----

# PEP 426: Inherited from setuptools

* Refined and enhanced `extras` system (more on that shortly)

----

# PEP 440: Version specifiers

* Based on the specifiers and scheme in PEP 345 and 386
* Added "compatible release" specifiers: `other (X.Y)`, `other (~= X.Y)`
* Added "prefix matching" specifiers: `other (== X.Y.*)`
* Added "direct reference" specifiers: `other (is https://exact-ref.com/file)`
* Only final and post releases considered by default
* Sort order changed to match setuptools

----

# PEP 426: Semantic dependencies

* Splits dependencies into 5 categories: meta, run, build, test, dev
* `meta_requires`: redistribution of exact versions of other components
* `run_requires`: runtime dependencies
* `build_requires`: build dependencies
* `test_requires`: test suite execution dependencies
* `dev_requires`: other tools needed by project developers
* Deliberately avoids reusing existing setuptools names

----

# PEP 426: Conditional dependencies

* Corresponding `*_may_require` field for each `*_requires` field
* Can use environment markers to indicate when the dependency is needed
    * Operating system
    * Python version
    * Various other conditions
* `setuptools` style "extras" system

----

# PEP 426: Enhanced extras system

* `project`: installs distribution, `:run:` and `:meta:` dependencies
* `project[opt]`: also installs dependencies flagged with the `opt` extra
* `project[-,:build:]`: just the build_* dependencies
* `project[-,:*:]`: just the dependencies, not the project

----

# PEP 426: Install hooks

* Based on setuptools entry point notation (`module.name:callable.name`)
* Allows code to be executed after installing and before uninstalling a
  wheel rather than relying on `setup.py install`
* Distribution metadata is passed directly to the hook implementations

----

# PEP 426: Metadata extensions

* Extension mechanism to record arbitrary settings in the metadata
* Can be used to record additional settings for the benefit of metabuild
  hooks

----

# What about the standard library?

* At least need the `pip` bootstrapping system in Python 3.4
* *May* propose `distlib` for inclusion (depending on maturity)
* Likely won't see an alternate build system until 3.5 at the earliest

----

# Other future plans

* PEP to define general purpose entry points as a metadata 2.x extension
* PEP to define the metabuild system as a metadata 2.x extension
* Supporting custom importers when retrieving installation database entries
* Considering "The Update Framework" as a tool to support optional end-to-end
  package signing that addresses the systemic vulnerabilities in the SSL CA
  system and avoids the need to treat PyPI as a trusted server
    * https://www.updateframework.com/

----

# Python Packaging Authority resources

* Documentation:
    * https://python-packaging-user-guide.readthedocs.org/en/latest/
    * Also covers getting involved and sketches out future plans
* Source code:
    * https://bitbucket.org/pypa/
    * https://github.com/pypa/
* Mailing lists:
    * http://mail.python.org/mailman/listinfo/distutils-sig
    * https://groups.google.com/forum/?fromgroups#!forum/pypa-dev

----

# Q & A

Questions about 3.4 plans are fair game, too :)

Presentation source:

    https://bitbucket.org/ncoghlan/misc/src/default/talks/2013-pyconau/packaging

Presentation tools:

* landslide: ``pip install landslide``

----

# Investigating Perl's CPAN

* Predates even `distutils`
* Authors must register on PAUSE
* PAUSE analyses uploaded modules prior to publication to CPAN
* `setuptools` version comparison is quite similar to Perl's
* Aimed primarily at system administrators and other command line users
* The `XS` C extension build system isn't needed for pure Perl installs
* Perl-on-Windows is a separate effort from core Perl development
* Building extensions on Windows requires GNU tools

----

# Investigating Ruby's Gems

* Similar vintage to `setuptools`
* While gem files are full Ruby files, they make *multiple* calls to
  the gem infrastructure, rather than one big `setup` call
* As with Perl, building extensions on Windows requires GNU tools
* `bundler` for installation

----

# Investigating PHP's PEAR and Composer

* PEAR
    * Similar vintage to `distutils`
    * Curated collection of packages rather than PyPI's "anything goes"
    * Batch file for bootstrapping on Windows
    * System wide installation
* composer
    * Recent creation (2011)
    * Application specific dependencies (akin to Ruby's `bundler`)

----

# Investigating Node.js

* npm (Node.js)
    * Relatively recent creation (2009)
    * Uses node-gyp (Python!) to handle cross-platform building by generating
      vcxproj files on Windows and a suitable Makefile everywhere else

----

# Other significant dates

* CPython migration to Sourceforge: May 2000 (http://docs.python.org/2/whatsnew/2.0.html)
* CPython migration to Subversion: ~July 2004 (PEP 347)
* CPython migration to Mercurial: ~May 2009 (PEP 385)
* First `pywin32` commit: August 1999 (http://pywin32.hg.sourceforge.net/hgweb/pywin32/pywin32/rev/c7addbf9ddf5)

----

# Random other notes

* Other things of a similar age:
    * Creation of the Open Source Initiative (early 1998)
    * Founding of Google (September 1998)
    * Akamain founding (April 1999)
* Development process and governance maturity:
    * Creation of the Python Enhancement Proposal process: March 2000
* Creation of the Python Software Foundation (March 2001)
* Red Hat Enterprise Linux v2.1: March 2002
    * yum provided in Fedora Core 1
    * up2date dropped in Fedora Core 5 and Red Hat Enterprise Linux 5
* Unicode:
    * Added in Python 2.0 (around the same time as distutils)
