# Nobody Expects the Python Packaging Authority

----

# Who am I?

## Nick Coghlan (@ncoghlan_dev)

* CPython core developer since 2005
* Nominated member of the Python Software Foundation
* Red Hat toolsmith
* "BDFL Delegate" for packaging related PEPs

----

# Python packaging is `______`?

# Presenter Notes

* The newcomer's lament
* "Why is Python packaging so bad?"
* They're not wrong
* Especially compared to more modern tools like npm (Node.js)
* Important questions
    * Where are we now?
    * Where do we want to be?
    * What's stopping us from getting there?
    * What can we do about it?

----

# 15 years of<br/>Python packaging

# Presenter Notes

* `distutils` (December 1998)
* `setuptools`/`easy_install` (March 2004)
* `virtualenv` (September 2007)
* `pip` (October 2008)
* `distribute` (July 2009)

* `distutils`: "Distribution is a platform problem"
* Primarily a build system
* Minimal distribution and installation support
* About the same age as Google (September 1998)

* `setuptools`: "Distribution is a language problem"
* Tricky to integrate with Linux distros
* Failures tend toward the cryptic

* `virtualenv` and `pip`: "Separate the application from the platform"
* Created September 2007 and October 2008 respectively
* Eliminated many `setuptools` quirks
* Added drawbacks of their own (no binary format!)

* `distribute`: setuptools fork

* `distutils2` as a detour

----

# Where do we<br/>want to be?

# Presenter Notes

* Clear, authoritative guidelines for newcomers to Python
* Easy for newcomers to get started with the recommended tools
* Fast, reliable and reasonably secure tools for sharing distributions
* Interoperate cleanly with platform-specific distribution systems

----

# Goal 1<br/>Clear, authoritative<br/>guidelines

----

# What prevents<br/>clear guidelines?

# Presenter Notes

* Who decides?
* Which tools?
* Which docs?

* Who can say "Yes, let's do that?"
* `setuptools` vs `distribute`
* `pip` vs `easy_install`
* How do users identify the "official" guidelines?

----

# The power to say<br/>"Yes"

# Presenter Notes

* Borrowing the authority of Guido van Rossum, Python's BDFL
* Packaging standards captured as PEPs
* Final decisions made by:
    * Richard Jones (for the Python Package Index)
    * Me (everything else packaging related)
* We're just the ones who say "Yes, let's do that"
* The folks doing most of the heavy lifting are the leaders and
  developers on the individual projects


----

# Ecosystem first<br/>standard library later

# Presenter Notes

* Discussion on distutils-sig, NOT python-dev
* Ecosystem first, standard library later
* Changed the PEP process to support this approach

----

# `setuptools` vs<br/>`distribute`

# Presenter Notes

* `distribute` *was* a popular `setuptools` fork
* improvements have been merged back as `setuptools` 0.7
* `distribute` 0.7 depends on `setuptools` 0.7
* some pip/virtualenv compatibility hiccups with 0.7
* Answer will soon be simple: use `setuptools (>= 0.8)`

----

# `setuptools 0.8+`

----

# `pip` vs<br/>`easy_install`

# Presenter Notes

* `easy_install` has a lot of problematic default behaviours
* `pip` avoids most of those problems
* Lack of binary distribution support is a big issue on Windows
* Added in latest version based on the PEP 427 `wheel` format
* Answer is now simple: use `pip (>= 1.4)`

----

# `pip 1.4+`

----

# Who do you believe?

----

# The Python Packaging<br/>Authority!

# Presenter Notes

* Already the home of `pip` and `virtualenv`
* Now also the home of `setuptools`, `pypi`, and `distlib`
* Creating https://python-packaging-user-guide.readthedocs.org
* Will add links from docs.python.org once guide stabilises
* Nearer term, aim to improve pip-installer.org

----

# The "Science!" exception

# Presenter Notes

* For most software, potentially integrating with system package
  managers and allowing low impact security updates is important
* For scientific software, being able to reliably reproduce a
  specific software stack is more critical
* The combination of hashdist (build) and conda (installer) handles
  this better than setuptools and pip ever will
* zc.buildout is another tool for managing complete application stacks
  independent of system package management tools

----

# Goal 2<br/>Make it easy to<br/>get started

----

# `pip` in the<br/>standard library?

# Presenter Notes

* Essentially, yes!
* Aim is to have pip available by default with Python 3.4
* Bootstrap command included in standard library
* Run explicitly for custom source builds
* Run automatically by Windows and Mac OS X installers
* Work with distros to arrange this for Linux
* Optionally retrieves pip from PyPI
* Easier to handle security updates that way
* pyvenv will be able to make pip available automatically (like virtualenv)
* Also key to PEP 431 (improved time zone support)
* No published PEP yet. PEP 439 is a different scheme that we don't
  think will work because pip and the OS package manager will get
  into a fight about who owns which files

----

# What about 2.7? 3.3?

# Presenter Notes

* Bootstrap scripts will have a home on PyPI
* This just makes current bootstrap mechanisms more official
* Standard packaging user guide should also help

----

# Goal 3<br/>Fast, reliable, and <br/>reasonably secure

----

# What prevents<br/>fast distribution?

# Presenter Notes

* Complex opt-in mirroring system
* Scanning external links
* Downloading distributions to read metadata

----

# Content Delivery Network<br/>(donated by Fastly)

# Presenter Notes

* Reduced load on the master PyPI server
* Used automatically, no need for tool support
* Usual geographic distribution benefits of a CDN
* Also giving us the access needed to maintain download counts

----

# Eliminating scanning<br/>of external links

# Presenter Notes

* PEP 438 has started migration away from scraping of external links
* Off by default for new projects
* Switched off automatically for projects that didn't need it
* Project authors can explicitly switch it off
* External links can be added manually if needed
* http://pypi-externals.caremad.io/

----

# Binary distribution with `pip`

# Presenter Notes

* pip has long had download caching
* pip 1.4 enables binary distribution for Windows
* also allows build caching for other platforms

----

# Metadata 2.0!<br/>(PEP 426 & 440)

# Presenter Notes

* Also want PyPI to publish full metadata
* Goal of the current PEP 426/440 metadata 2.0 standard
* JSON based for easy web publication

----

# What prevents<br/>reliable distribution?

# Presenter Notes

* PyPI stability issues
* External hosting of files adding more points of failure
* Complex mirroring system

----

# Migration to OSU/OSL

# Presenter Notes

* PyPI relocated to better provisioned systems at OSU/OSL

----

# Faster *and*<br/>more reliable

# Presenter Notes

* Avoiding external hosting means fewer points of failure
* Even if PyPI goes down, CDN is configured to keep responding

----

# What about the PyPI mirrors?

# Presenter Notes

* For a long time, the public mirrors *did* help
* More recently, many problems with stale mirrors
* Mirror autodiscovery scheme is inherently insecure and is in the process
  of being removed (needs to be done slowly to avoid breaking things
  without adequate warning - PEP 449 has details)

----

# Long live the PyPI mirrors

# Presenter Notes

* There is no SLA for PyPI! Free service funded by the PSF,
  OSU/OSL and Fastly
* Run at least a caching mirror if PyPI is critical to you
* devpi and localshop are good tools for this
* bandersnatch is the recommended client for full mirrors
* Register with pypi-mirrors.org (just a list, no replacement
  autodiscovery mechanism at this point in time - likely won't
  be until we have package signing or an equivalent)

----

# What prevents (reasonably)<br/>secure distribution?

# Presenter Notes

* Tools using HTTP by default
* Issues with domain suffixes and wildcards
* Vulnerabilities in the mirroring system
* A lot of trust placed in PyPI's integrity

----

# PyPI security improvements

# Presenter Notes

* PSF has now acquired a High Assurance SSL cert
* Forced HTTPS by default for browser based PyPI interactions
* Docs hosting moved out to a separate *.pythonhosted.org domain
* All of python.org will eventually switch to forced HTTPS

----

# Client security improvements

# Presenter Notes

* `pip` added SSL verification in 1.3
* `easy_install` added it in setuptools 0.7

----

# Can PyPI mirrors<br/>be trusted?

# Presenter Notes

* If they only serve files over HTTP, then definitely not
* If they use HTTPS, then maybe
* These days, the simplest trust chain is PyPI, the Fastly CDN and a PyPI
  mirror you control. Using a third party mirror probably isn't the
  best way to try to achieve additional reliability.
* Running your own mirror may still be worth it

----

# Can *PyPI* be trusted?

# Presenter Notes

* Using SSL for security places a lot of trust in the integrity of PyPI

* If you can avoid trusting PyPI, don't.
    * Set up a private mirror. Audit your packages.
* This kind of thing is one of the reasons people pay platform vendors

* At the tool design level, not trusting PyPI is a much harder problem
* "The Update Framework" looks promising
* Making The Update Framework easier to use is a simpler problem than
  devising a different secure distribution system
* However, key distribution remains a fundamentally hard problem
* They do have a proof of concept up and running
* Near term, the focus is on SSL rather than end-to-end signing
* Metadata 2.0 includes some basic hashchecking options

----

# Goal 4<br/>Better platform<br/>interoperability

----

# Developers: Cross platform<br/>tools rock!

# Presenter Notes

* Same commands on Linux, Mac OS X, Windows

----

# Integrators: Language neutral<br/>tools rock!

# Presenter Notes

* C, C++, Java, Python, Perl, Ruby, Javascript, Haskell
* Erlang, Rust, Go, ...
* New distribution tools --> new security vulnerabilities
* Auditing and certification still matter

----

# We want to<br/>support both

# Presenter Notes

* Python specific tools by default
* Support translation to platform tools
* This is part of the new world order in PEP 426/440 :)
* Scientific toolchains are just another platform for the
  PyPA tools to interoperate with

----

# Q & A

Presentation source:

    https://bitbucket.org/ncoghlan/misc/src/default/talks/2013-pyconau/packaging

Presentation tools:

* landslide: ``pip install landslide``
* avalanche: https://github.com/akrabat/avalanche

----

# PyPA documentation

* [Python Packaging User Guide](https://python-packaging-user-guide.readthedocs.org/en/latest/)
* Also covers getting involved and sketches out future plans

----

# PyPA source code and issue tracking

* [GitHub](https://github.com/pypa/)
    * `pip`, `virtualenv`
* [BitBucket](https://bitbucket.org/pypa/)
    * `setuptools`, `pypi`, `distlib`, `pylauncher`

----

# PyPA mailing lists

* [distutils-sig](http://mail.python.org/mailman/listinfo/distutils-sig)
* [pypa-dev](https://groups.google.com/forum/?fromgroups#!forum/pypa-dev)
