= Python Beyond (C)Python: Adventures in Software Distribution =

== The Power of Ubiquity ==

You aren't going to find technologists waxing lyrical about the design
and architecture of languages like shell script, Javascript, C and Java.

Yet all of these are *incredibly* popular development languages. Why?
Ubiquity. Every POSIX based operating system can run shell scripts. Every
web browser can run Javascript. Every Microsoft Office installation is a
VBA runtime, C is essentially cross platform assembly code, and Sun
successfully stormed the gates of the enterprise and tertiary education in
their original all out push for Java dominance.

Ubiquity has a tendency to create self-reinforcing cycles. When something
is already ubiquitous, people rely on it being there, so it becomes ever
harder to take it away. When something is likely to be encountered, knowing
how to use it can be a valuable skill, so more opportunities to learn it are
likely to be made available. As more people rely on it, it becomes more
valuable to spend time improving it, so it becomes better to work with, and
even *more* people are likely to start learning and using it.

== The Role of Redistributors ==

When you look at ubiquitous development languages, one key feature they
share is an extremely robust ecosystem of redistributors that don't provide
the language for its own sake, but because it serves their interests to do
so.

Shell script and C together provide the essential interfaces for working
with POSIX operating systems. Web browser vendors don't ship Javascript to
let end users write their own Javascript applications, but to execute
dynamic content on web sites. Java application server vendors can target
users of *any* operating system, rather than being limited specifically to
UNIX, Linux or Windows.


= Distribution & Discoverability =

How do people discover Python?

- part of their operating system
- scripting engine in another application (e.g. Maya, Scribus)
- offered by a platform of interest
- implementation language of a notable application (OpenStack, IPython, YouTube, EdX)
- word of mouth
- Software Carpentry and other "Learn to Program" workshops
- early educational activities (OLPC, Raspberry Pi Foundation)
- tertiary education (introductory computer science courses)
- as part of learning something else (scientific Python stack, Arduino control)


How do people install Python?

- provided as part of their operating system (Mac OS X, Linux)
- direct from python.org (Windows, Mac OS X)
- via a redistributor (ActivePython, Canopy, Anaconda, Python(x,y), Software Collections)
- Platform-as-a-Service (Google App Engine, Heroku, OpenShift, Stackato, etc)
- in the browser (PythonAnywhere)
- build from source

How do people work with Python?

- text editor and CLI? (*cough*)
- IDLE?
- Python specific IDE? (PyCharm, Wingware, Komodo, etc)
- Plugin for larger IDE? (PyDev, PTVS)
- IPython shell? GUI? Notebook?
- scientific workspaces? (Python (x,y), Canopy,

How do people discover & install alternate Python implementations?

- Stackless
- IronPython
- Jython
- PyPy


Continuum Analytics stats:

Nov 13 - May 14 Mac     Windows Linux
Anaconda        27.9%   56.1%   16.0%
Miniconda       3.8%    7.7%    88.5%
Miniconda3      11.4%   36.3%   52.1%


Distro stats:

Fedora 20

$ repoquery --whatrequires --recursive python | wc -l
15107

Jorgen Schäfer ‏@JorgenSchaefer 8m

@ncoghlan_dev Current Debian Testing: apt-rdepends -r python | wc -l -> 16477. Not sure if those commands are fully equivalent, though.


iPad apps/environments:

http://computableapp.com/
http://omz-software.com/pythonista/

