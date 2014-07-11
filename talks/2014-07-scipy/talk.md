# Python Beyond (C)Python:<br/>Adventures in<br/>Software Distribution

# Presenter Notes

* get to software distribution in a moment
* short detour regarding the adoption of programming languges and other
  tools for thinking.

---

# Proposition:<br/>design is the key determining factor in language adoption

# Presenter Notes

* this is something technologists generally assume to be true
* it's worth asking if experience backs up that assumption

---

# C++<br/>Java<br/>Javascript<br/>Shell syntax<br/>

# Presenter Notes

* none of these are especially well designed
* all of them are *incredibly* popular development languages. Why?

---

# Footholds<br/>and ...

# Presenter Notes

* every POSIX based operating system can run shell scripts
* every web browser can run Javascript
* C is essentially cross platform assembly code
* Sun successfully stormed the gates of the enterprise and tertiary
  education in their original all out push for Java dominance.

---

# ... positive<br/>feedback<br/>loops

# Presenter Notes

* ubiquity creates self-reinforcing cycles
* assumed availability -> more likely to rely on it -> more likely to provide
* more reliance -> more opportunities to learn -> more likely to learn
* more widely used -> greater investment -> better tools -> more likely to use

---

# Gaining a<br/>foothold

# Presenter Notes

* once the positive feedback loops kick in, starting point can be irrelevant
* getting to the starting line is still hard
* the blessing of a high profile platform vendor (think Microsoft with VBA
  and C#, Apple with Objective-C and Swift, or even Sun with Java) can
  make a big difference
* PHP isn't likely to win any language design awards either, yet its
  popularity with early hosting providers was enough to secure it a
  significant place in the modern computing environment
* yet I think there's an even better example of this process in action

---

# Office<br/>"productivity"<br/>suites

# Presenter Notes

* Spreadsheets are a terrible programming tool
* no testing, no code review, bad version tracking

* I bet more data analysis done with Excel than in all programming languages
  combined
* perhaps not by data volume, but by number of analysts

* spreadsheets make tasks like adding up a series of numbers truly simple
* they build from there to full-fledged applications
* even professional software developers can't maintain complex spreadsheets
  properly, as they're out of reach of our maintenance tools


---

# Whither<br/>Python?

# Presenter Notes

* Python already has footholds in a wide array of domains
* system orchestration, Linux system management, scientific computing,
  financial analysis, education from elementary through to tertiary,
  artistic endeavours, especially animation

* the question now is how to kick the positive feedback loops into high gear
* how do we take the vast array of technology we have and make accessing it
  as simple and easy as opening up our spreadsheet program, loading up a
  CSV and clicking a few buttons to create a pretty chart?

---

# Software distribution:<br/>an unsolved problem

# Presenter Notes

* software distribution is an unsolved problem, not just in the Python
  community, but in software engineering in general
* operating system vendors struggle to provide good packaging and deployment
  experiences for developers that *solely target that platform using the
  vendor's recommended and specifically supported programming languages*
* this is a problem that professional developers find hard enough that we
  always end up constraining it in some way
* language specific, platform specific, domain specific


---

# CPython:<br/>our community's<br/>most successful product

# Presenter Notes

* users have many options for getting CPython through channels that
  are convenient for *them*
* build from source (tarball, Mercurial, git mirror)
* binary download from python.org for Mac OS X and Windows
* Linux distros (community and commercial)
* Mac OS X system Python & package managers (homebrew, Fink, MacPorts)
* commercial vendors (Enthought, Continuum Analytics, ActiveState)
* Platform-as-a-Service providers (Google App Engine, Heroku, OpenShift)
* Online offerings (PythonAnywhere, wakari)
* Other platforms (iOS apps, Chrome native apps)
* Embedded as the scripting engine in a wide range of applications, most
  notably animation tools like Blender and Maya3D
* we don't have anything else that even comes close to the breadth of
  distribution of CPython

---

# Redistributors are<br/>not the enemy!

# Presenter Notes

* users *like* redistributors - consistent interfaces, integrated software
* redistributors extend the overall reach of the Python community
* problem: domain specific redistributors tend to offer only a subset of
  packages.
* Linux distros missing data analysis packages, analysis environments missing
  security software
* this can make collaboration across domains undesirably difficult
* to improve, focus on users: provide what they want, when they want,
  how they want
* when users don't have a preferred redistributor, we should provide a
  default community driven one
* but when they *do* have an existing redistributor they like, that becomes
  a design constraint

---

# The Python<br/>Packaging<br/>Authority

# Presenter Notes

* originally created as a shared home for pip and virtualenv
* a bit over a year ago, I proposed making it a home for all of the projects
  working together to improve the Python packaging ecosystem
* in addition to pip and virtualenv, now home to pypi, wheel, setuptools, the
  Python launcher for Windows, distlib, the bandersnatch mirroring client,
  the Python packaging user guide and the packaging metadata 2.0 effort
* visit packaging.python.org for more info

---

# Feeding the existing<br/>distribution channels

# Presenter Notes

* emphasis in the Python Packaging Authority is that we want to work *with*
  our redistributors, rather than against them
* the default tools are designed with that in mind
* aim is to allow redistributors, if they so choose, to *automatically*
  convert the whole of PyPI to their preferred formats
* that's a key focus of our metadata 2.0 efforts - tightening the constraints
  on the PyPI metadata, making it more expressive, while ensuring we provide
  suitable escape hatches to deal with legacy packages that don't yet comply
  with the updated guidelines

---

# pypi<br/>pip<br/>setuptools<br/>wheel

# Presenter Notes

* learned from distutils2 experience that proposals without a workable
  transition plan for the 45k existing packages on PyPI will fail
* having tool developers collaborating as part of PyPA is a key part of
  making this feasible at all
* the automated conversion goal *does* drive up the complexity of the
  upstream tooling
* aim is to allow choice of packaging system to be driven by user preference
  rather than packaging availability
* encourage redistributors interested in this to join distutils-sig to
  participate in discussions

---

# Politics and<br/>commerce

# Presenter Notes

* Redistributors serve a purpose, but we're still commercial operations
* What we ship and support is going to be driven by our own interests,
  not upstream goals
* this is open source, though, so we can also go around redistributors,
  rather than through
* I encourage anyone getting CPython from a commercial redistributor,
  including Linux distros, to let their vendor know whenever they have to
  go around them and retrieve software directly from upstream
* it's hard to go past customers asking about things engineering teams were
  already interested in shipping as a way to get redistributors to act

---

# Where<br/>redistributors<br/>fall short

# Presenter Notes

* within a Python installation, pip and virtualenv can handle
  redistributor shortfalls
* don't help with managing and updating the Python runtime and external
  dependencies, especially when you don't have admin rights
* Windows is a major market - 35 millions installer downloads a year from
  python.org alone
* it would be convenient if there was a completely open source tool that:

    * worked much the same way across Windows, Mac OS X and Linux
    * could be used to manage the underlying Python runtime like any other
      package
    * could be used to manage arbitrary external dependencies in any language
    * could be used even without admin access to the machine

---

# conda:<br/>a cross-platform<br/>platform

# Presenter Notes

* open source project originally created and released by
  Continuum Analytics
* trades reduced integration with the OS for greater cross platform
  consistency
* valuable option for end users looking for user level installations that
  work cross platform independently of the system Python
* less interesting to redistributors (except as a competitive threat)
* not a PyPA project (since it isn't Python specific), but recommended as an
  open source cross platform dependency management system designed with the
  needs of Pythonistas in mind
* for example, it is already designed to interoperate transparently with pip
  and PyPI

---

# The<br/>Linux distro<br/>perspective

# Presenter Notes

* switching hats from Python packaging BDFL-delegate to Linux advocate
* one of a Linux vendors core tasks is to act as a curator and gatekeeper
  for open source packages
* open source world is inherently populated by early adopters
* Linux distros help bridge the gap to more conservative users
* even the most conservative user occasionally wants a more recent
  version of "just that one package"
* historically, our focus on security and sustainability concerns have meant
  that we, as distros, haven't done a particularly good job of addressing
  that need

---

# Unlocking<br/>the distro<br/>gates

# Presenter Notes

* programming language communities often try to bypass the Linux distro
  review processes
* Fedora has 15k packages that depend on Python, Debian around 16k,
  vs 45k on PyPI
* also no guarantee that the packaged versions are being kept up to date
* this can leave users in a bad place, as they're forced to:
    * ignore all the software that isn't in their preferred channel
    * abandon their platform tools entirely, even if they're otherwise
      happy with them
    * attempt to straddle two different packaging systems
* this is a problem the Linux distros themselves are now trying to better
  address

---

# (Linux) repos<br/>as a service

# Presenter Notes

* Ubuntu has long had Personal Package Archives, where it is possible to
  upload source packages and Launchpad takes care of publishing a valid
  apt repository
* Fedora has recently added the COPR build system to make it easier to
  publish custom repos not only for Fedora, but also for RHEL and CentOS
* Just this week, Slavek, the lead Python maintainer for Fedora & RHEL,
  announced a COPR with nightly builds for Python 3.5
* the Fedora Playground concept
  (https://fedoraproject.org/wiki/Changes/Playground_repository) aims to
  go beyond PPAs in terms of integrating with the underlying operating
  to make COPR repos easier to manage for users, and provide a clearer
  pathway into the distribution for new packages that may not meet distro
  guidelines yet

---

# Software<br/>collections

# Presenter Notes

* equivalent of virtualenv for the system package manager
* allows access to newer language runtimes, databases and web servers,
  without interfering with the versions integrated into the underlying OS
* the upstream community has been seeded with collections Red Hat created
* core design concepts should be applicable to any system package manager
* current tools are RPM specific - more work is needed to get
  apt-based collections up and running
* this is what Slavek is using to provide Python 3.5 nightlies for Fedora
  without messing with the system installation of Python 3
* still relatively new, so there's an opportunity for the
  scientific Python community to guide the evolution in
  directions that work for data analysis environments, not just for web
  application deployment.

---

# Portable<br/>execution<br/>environments

# Presenter Notes

* the problem of reproducible analysis environments in science has a
  lot in common with repeated application deployments in professional
  software development
* in the professional software world, we want development, integration,
  testing, staging and production environments to be as consistent as
  possible
* in the data analysis world, the main aims are to make it easy for analysts
  to get started, but also to make it easy to check someone else's work
* this is not a solved problem in general!
* Platform-as-a-Service is one approach, but it's very, very specific to
  stateless web applications
* Virtual machines are more flexible, but resource hungry & hard to keep
  up to date

---

# Docker<br/>containers

# Presenter Notes

* in the Linux world, one of the most promising technologies in this
  space is application containers
* in particular, Docker containers are an emerging standard with broad
  cross distribution support
* the same tech that professional developers use to get local testing
  environments could be used to transport, for example, a fully
  configured IPython notebook environment, which can then be run on any
  modern Linux distro with full container support
* Docker handles *running* the container images, but doesn't have a lot to
  say about how to define them in the first place
* in the Python world, tools like hashdist and conda environments can
  potentially tie in nicely with containers, since they can cover the
  non-Python components as well
* there's a major opportunity for the scientific Python community here, as
  many of these design discussions are currently dominated by Software-as-a-Service
  web application developers. Getting the data analysis community more
  involved could help ensure we don't see a repeat of the current state
  of Platform-as-a-Service offerings.

---

# Following Linux<br/>across the chasm!

# Presenter Notes

* For anyone not aware, "the chasm" is a marketing concept describing the
  difficulty of getting any technology or product beyond the early adopter
  community and into the hands of mainstream users
* Most open source and academic languages fail to make that leap
* I'm told Python recently overtook Java as the most taught language in
  US introductory CS course
* Python, like Linux, has quietly made its way into a vast array of companies
* The rise of OpenStack is bringing unprecedented corporate attention to bear
  on the Python community
* The opportunity before us as a community is enormous, we just need to take
  it!
* I think offering a world class software distribution system is a key part
  of that, but...

---

# Help needed!

# Presenter Notes

* filling in the rough notes and blanks on packaging.python.org
* distutils-sig and the PyPA communities on GitHub and BitBucket
* the conda community on GitHub
* investigate the potential for integration with Linux technology
  like software collections and Docker containers
