---
title: CPython Core Development
theme: beige
---

### (Getting Into)
## CPython Core Development

Nick Coghlan (@ncoghlan_dev)

CPython core developer<br/>(since 2005)

---

### The CPython Code Base

* Total commits: 100k+ (Github stats)
* Total contributors: 1760+ (Misc/ACKS)
* First commit: August 5th, 1990 (~27 years ago)
* Python lines: ~530k code, ~120k comments
* C lines: ~390k code, ~50k comments

Note:

* Where to start?


---

### Start with "Why?"

Note:

* Python core development covers a broad range of activities
* Your personal motivations for getting involved thus have a big
  impact on where it makes sense to start
* Participation is mostly about intrinsic rewards rather than external
  ones, so knowing why you started is also key to knowing when to stop

---

### Acknowledge the timelines

* Maintenance releases ~6 months
* Feature releases every 18-24 months
* Redistributors may add weeks or months of latency
* Platforms may add years of latency (e.g. LTS Linux)
* Workflow tools aspire to continuous deployment!

Note:

* CPython's release cadence is not fast, so if you're looking for instant
  gratification, contributing to the workflow tools may be of more interest
  than CPython itself
* Personally, I find the slow cadence relaxing - there's almost always time to
  discuss ideas and consider them from multiple angles, and because there
  aren't any road map commitments, we can always slip changes to a later release
* The maintenance process for the workflow tools also more closely resembles
  typical network service development in an organisation, whereas a language
  runtime like CPython faces all sorts of additional considerations

---

### Patience is Required

Note:

* While some core developers do get paid to contribute to CPython, they're
  usually only paid to focus on specific features and bug fixes of interest
  to their employers
* This means mentoring new contributors comes out of people's personal time,
  and hence may only be intermittently available
* Meeting core devs in person, whether at a post-conference development sprint,
  or a local meetup like this one, tends to help get priority attention for
  the time we devote to that task
* Aside from that, you're relying on a combination of luck (sometimes an issue
  report just happens to catch our interest), self-interest (we're more likely
  to follow up if someone tries to resolve an issue we reported), and explicitly
  assumed responsibilities (modules with designated experts in the developer
  guide are more likely to receive attention)

---

## Some<br/>Motivations

Note:

* I can't even conceive of all the possible reasons someone might want to
  contribute to CPython, but there are a few recurring ones
* So I'll present this in the form of example motivations, and some steps
  towards get started given that motivation

---

### The docs have this<br/>minor error...

Note:

* Simple documentation fixes are one of the easiest places to get started,
  simply because you can do it entirely through the web browser

---

### Step 1:<br/>Find the source page on GitHub

Note:

* CPython's source repo is on GitHub these days, and one of the main benefits
  that offers is through-the-browser editing for documentation fixes
* The Doc directory layout mirrors the HTML layout on docs.python.org

---

### Step 2:<br/>Make your edits

Note:

* Once you find the page of interest, you can hit the Edit icon, and Github
  will automatically fork the repo and create a working branch for you
* The in-browser text editor isn't wonderful, but it's good enough for basic
  tasks link typo fixes, updating links, and so forth
* For more complex updates, documentation updates are handled like any other
  bug (which I'll get into next)

---

### Step 3:<br/>Submit your PR

Note:

* Once your finish your edits, GitHub lets you easily turn them into a PR
  against the main CPython repo
* This will kick off several automated checks, and will complain that a NEWS
  entry and issue reference are missing. For simple typo fixes, the reviewer
  will add labels to tell the bot that's OK. For more complex changes, the
  reviewer may ask you to create an issue explaining the motivation for the
  change.

---

### I have this bug...

Note:

* When your Python code is broken, you probably *haven't* found a bug in
  the interpreter or the standard library
* Nevertheless, our open issue count is already over 6000, and it's steadily
  growing
* Ensuring that future you doesn't have to deal with the same problems as
  current you is a time-honoured motivation for getting involved in an open
  source project

---

### Step 1:<br/>Build CPython

Note:

* This step is the main focus of the Quick Start at the beginning of the
  CPython Developer Guide (I'll provide a link to that at the end)
* The Quick Start aims to take you through the process of cloning the main
  CPython git repo, building it locally on Windows, Mac OS X, or Linux, and
  then running the test suite to make sure your build works

---

### Step 2:<br/>Add a new test case

Note:

* All the tests live in Lib/tests, even those that are testing base
  interpreter functionality
* Confusingly, the test layout still mostly follows the Python 2.x stdlib
  layout, since it's a lot easier to break things without noticing when
  refactoring tests than it is when refactoring tested code
* I mostly just look for existing tests that call into the code I'm intending
  to change, and fit my new test case in there
* Almost all of the tests are written in Python
* It can be helpful to post your draft test case to whatever issue you're
  trying to fix, in order to get feedback on whether or not it actually
  specifies the desired behaviour

---

### Step 3:<br/>Make the change

Note:

* Regardless of whether or you do that or not, the next step is to actually
  make the change
* The pure Python code for the standard library is all in the Lib subdirectory
* The C code is split across Programs, Python, Objects, and Modules, and the
  distinctions between the latter 3 can get a bit blurry
* Code searching tools are an essential aid. I personally use Eli Bendersky's
  pss utility, but anything that will let you easily search a directory tree
  for all occurrences of a particular symbol will do the trick

---

### Step 4:<br/>Submit your PR

Note:

* There are a few more steps to this when it comes to code changes, but the
  developer guide takes you through the process
* The big difference is that you have to push your local changes up to your
  CPython fork on GitHub, then submit the PR based on that

---

### I'm curious<br/>and I learn by doing...

Note:

* Sometimes folks are interested in participating in core development, but
  first need to find something interesting to work on


---

### Step 1a:<br/>look for "easy" bugs

Note:

* The issue tracker has a link on the sidebar for "easy" issues. These are
  issues that are considered sufficiently well-defined that a new contributor
  can take them on with the assistance of the developer guide
* We also have a separated tag for easy C issues, since they may be easy for
  folks that already know C, but they're decidedly *not* easy if you need to
  learn it in the process
* This option is especially appropriate for folks that are not only new to
  CPython core development, but also new to software development in general

---

### Step 1b:<br/>look for old bugs

Note:

* For experienced developers, David Murray suggests an alternative approach,
  which is to browse the entire open issues list, starting with the *oldest*
  open issue
* These issues have usually been open for a long time for a reason, but reading
  the discussion can be quite educational, and sometimes you'll even find that
  they've actually been resolved since they were last looked at, but nobody
  went back and closed the issue

---

### Step 2:<br/>Proceed as for<br/>"I have this bug..."

Note:

* When you work on resolving an issue we usually don't ask too many questions
  about why you care
* "It looks interesting and it's been open for a long time" is just as valid a
  reason for caring as "I recently hit this in my own code"

---

### I'm more interested<br/>in the design process...

Note:

* This is how I personally became involved in the core development process
* I discovered comp.lang.python back when Usenet was still a thing, and from
  there discovered the python-dev mailing list
* Listening to folks like Tim Peters and Raymond Hettinger discuss trade-offs
  in the design of different data types, or Marc-Andre Lemburg and Martin von
  Loewis discuss Unicode was fascinating and educational, but it was something
  superficially trivial that got me to cross the line into becoming a
  contributor myself: creating the first version of the -m switch in order to
  make the timeit module easier to run from the command line
* Raymond Hettinger accepted the first version of that for Python 2.4, and then
  I helped out with benchmarking and iterating on the initial implementation of
  the pure Python decimal module (ask me about the integer conversion
  performance hack arising from that, and things grew from there

---

### Step 1:<br/>Browse the historical PEPs

Note:

* Python's design process has long been an open one, and since the release of
  Python 2.0 in 2000, major design decisions have been tracked through the
  Python Enhancement Proposal process
* Reading accepted and final PEPs can provide a guide as to which kinds of
  design arguments tend to be convincing
* rejected and withdrawn ones provide a repository of concepts which have been
  deemed unsuitable for Python (at least in the specific form presented by that
  particular PEP)
* open and deferred PEPs provide insight into currently open design questions

---

### Step 2:<br/>Sign up for python-dev

Note:

* This is the main list where items get escalated from the issue tracker if we
  can't come to a clear consensus on the suitability of a change there
* It's also the main list for final PEP reviews, where Guido or his delegate
  makes the determination on whether to accept a proposal or not
* Usually only moderate traffic, but can spike significantly when a particularly
  controversional proposal comes up and seems likely to be accepted

---

### Step 3:<br/>Sign up for python-ideas<br/>(optional!)

Note:

* This is a brainstorming list that's deliberately more receptive to outlandish
  ideas than the main python-dev list
* We set it up because even outlandish ideas can sometimes have a good idea, or
  at least a valid problem report, hidden inside them, but asking "Is there
  a potentially good idea here?" is a different question from python-dev's more
  abrupt "Is this a good idea for CPython at this point in time? Yes or no?"
* I find the list quite enjoyable most of the time, but you do need to be
  prepared to ignore threads that have devolved into esoteric silliness that
  has no chance of ever being accepted into the language

---

### Step 4:<br/>Sign up for python-checkins<br/>(optional!)

Note:

* This is a high traffic list that receives a notification for *every*
  accepted change into the CPython code base
* I read it consistently for several years after I became a core dev, but
  haven't even tried for the past few years
* If you have the time though, it can be an incredibly good way to get a sense
  of which parts of the CPython code base are being actively worked on, and
  who's specifically working on them

---

### I just want to help somehow...

Note:

* While CPython and standard library changes eventually reach an enormous
  audience, they'll often take years to get there
* Other projects are often more in need of help than we are, and any changes
  you contribute can be rolled out more quickly

---

### Idea 1:<br/>Python Packaging Authority

Note:

* CPython bundles the `pip` package manager
* packaging.python.org is the Python Packaging User Guide
* pypi.org is a deployment of the new Warehouse service intended to replace
  the legacy index service as pypi.python.org
* these projects affect a similarly broad audience to Python itself, but on
  a faster timeline, since they can be upgraded independently of the underlying
  Python version

---

### Idea 2:<br/>Roundup Issue Tracker

Note:

* This is the issue tracker that powers bugs.python.org
* Changes can be made either upstream (preferred), or specifically to
  the CPython deployment at bugs.python.org
* This handles a fair bit of the integration between GitHub and other python-dev
  and PSF workflows

---

### Idea 3:<br/>Buildbot CI Service

Note:

* This is the CI service that powers CPython's post-merge CI
* Allows us to test on architectures and operating systems beyond the basic
  set of Windows, Linux, and Mac OS X on x86-64 that cloud services offer

---

### Idea 4:<br/>PyPI Backports

Note:

* A number of standard library modules have counterparts on PyPI that provide
  access to APIs from later CPython releases on newer CPython versions
* Helping out with these can be a good way to build trust with a standard
  library module maintainer if there's a particular module you'd like to
  propose enhancements to


---

### Q & A

Source repo: https://github.com/python/cpython/

Developer guide: https://devguide.python.org/

Issue tracker: https://bugs.python.org/

PEPs: https://www.python.org/dev/peps/

Communications channels: https://devguide.python.org/communication/

Note:


* Here are the promised links
* Questions?
