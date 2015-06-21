.. _multicore-python:

Efficiently Exploiting Multiple Cores with Python
=================================================

:Published:    21st June, 2015
:Last Updated: 21st June, 2015

Both the Python reference interpreter (CPython), and the alternative
interpeter that offers the faster single-threaded performance for pure
Python code (PyPy) use a Global Interpreter Lock to avoid various problems
that arise with threading models that implicitly allow concurrent access to
objects from multiple threads of execution.

This has been the source of much debate, both online and off-, so this article
aims to summarise the design trade-offs involved, and give details on some
of the prospects for improvement that are being investigated.


Why is using a Global Interpreter Lock (GIL) a problem?
-------------------------------------------------------

The key issue with Python implementations that rely on a GIL (most notably
CPython and PyPy) is that it makes them entirely unsuitable for cases where
a developer wishes to:

* use shared memory threading to exploit multiple cores on a single machine
* write their entire application in Python, including CPU bound elements
* use CPython or PyPy as their interpreter

This combination of requirements simply doesn't work - the GIL effectively
restricts bytecode execution to a single core, thus rendering pure Python
threads an ineffective tool for distributing CPU bound work across multiple
cores.

At this point, one of those requirements has to give. The developer has to
either:

* use a concurrency technique other than shared memory threading
* move parts of the application out into non-Python code (the path taken
  by the NumPy/SciPy community, all Cython users and many other people
  using Python as a glue language to bind disparate components together)
* use a Python implementation that doesn't rely on a GIL (while the main
  purpose of Jython and IronPython is to interoperate with other JVM and
  CLR components, they are also free threaded thanks to the cross-platform
  threading primitives provide by the underlying virtual machines)
* use a language other than Python

Many Python developers find this annoying - they want to use threads *and*
they want to use Python, but they have the CPython core developers in their
way saying "Sorry, we don't support that style of programming".


What alternative approaches are available?
------------------------------------------

Assuming that a free-threaded Python implementation like Jython or IronPython
isn't suitable for a given application, then there are two main approaches
to handling distribution of CPU bound Python workloads in the presence of
a GIL. Which one will be more appropriate will depend on the specific task
and developer preference.

The approach most directly supported by python-dev is the use of
process-based concurrency rather than thread-based concurrency. All
major threading APIs have a process-based equivalent, allowing threading
to be used for concurrent synchronous IO calls, while multiple processes can
be used for concurrent CPU bound calculations in Python code. The
strict memory separation imposed by using multiple processes also makes
it much easier to avoid many of the common traps of multi-threaded code.
As another added bonus, for applications which would benefit from scaling
beyond the limits of a single machine, starting with multiple processes
means that any reliance on shared memory will already be gone, removing
one of the major stumbling blocks to distributed processing.

The main downside of this approach is that the overhead of message
serialisation and interprocess communication can significantly increase the
response latency and reduce the overall throughput of an application (see this
`PyCon 2015 presentation <http://pyvideo.org/video/3432/python-concurrency-from-the-ground-up-live>`__
from David Beazley for some example figures).

The major alternative approach promoted by the community is best represented
by `Cython`_. Cython is a Python superset designed to be compiled down to
CPython C extension modules. One of the features Cython offers (as is
possible from any C extension module) is the ability to explicitly release
the GIL around a section of code. By releasing the GIL in this fashion,
Cython code can fully exploit all cores on a machine for computationally
intensive sections of the code, while retaining all the benefits of Python
for other parts of the application.

`Numba`_ is another tool in a similar vein - it uses LLVM to convert Python
code to machine code that can run with the GIL released (as well as
exploiting vector operations provided by the CPU when appopriate).

This approach also works when calling out to *any* code written in other
languages: release the GIL when handing over control to the external library,
reacquire it when returning control to the Python interpreter.

.. _Cython: http://www.cython.org/
.. _release the GIL: http://docs.cython.org/src/userguide/external_C_code.html#acquiring-and-releasing-the-gil
.. _Numba: http://numba.pydata.org/


Why hasn't resolving this been a priority for the core development team?
------------------------------------------------------------------------

Speaking for myself, I came to Python by way of the unittest module: I needed
to write a better test suite for a C++ library that communicated with a
custom DSP application, and by using SWIG and the Python unittest module
I was able to do so easily. Using Python for the test suite also let me
easily play audio files out of the test hardware into the DSP unit being
tested. Still in the test domain, I later used Python to communicate with
serial hardware (and push data through serial circuits and analyse what
came back), write prototype clients to ensure new hardware systems were full
functional replacements for old ones and write hardware simulators to allow
more integration errors could be caught during software development rather
than only after new releases were deployed to the test lab that had real
hardware available.

Other current Python users are often in a similar boat - we're using Python
as an orchestration language, getting other pieces of hardware and software
to play nice, so the Python components just need to be "fast enough", and
allow multiple *external* operations to occur in parallel, rather than
necessarily needing to run Python bytecode operations concurrently. When our
Python code isn't the bottleneck in our overall system throughput, and we
aren't operating at a scale where even small optimisations to our software can
have a significant impact on our overall CPU time and power consumption costs,
then investing effort in speeding up our Python code doesn't offer a good
return on our time.

This is certainly true of the scientific community, where the heavy numeric
lifting is all done in C or FORTRAN, and the Python components are there to
make everything hang together in a way humans can read relatively easily.

In the case of web development, while the speed of the application server
may become a determining factor at truly massive scale, smaller applications
are likely to gain more through language independent techniques like adding a
Varnish caching server in front of the overall application, and a memory cache
to avoid repeating calcuations for common inputs before the application server
itself is likely to become the bottleneck.

This means for the kind of use case where Python is primarily playing an
orchestration role, as well as those where the application is IO bound
rather than CPU bound, free threading doesn't really provide a lot of
benefit - the Python code was never the bottleneck in the first place, so
focusing optimisation efforts on the Python runtime doesn't make sense.

Instead, people drop out of pure Python code into an environment that is
vastly easier to optimise and already supports free threading. This may be
hand written C or C++ code, it may be something with Pythonic syntax but
reduced dynamism like Cython or Numba, or it may be another more static
language on a preexisting runtime like the JVM or the CLR, but however it
is achieved, the level shift allows optimisations and parallelism to be
applied at the places where they will do the most good for the overall
speed of the application.


Why isn't "just remove the GIL" the obvious answer?
---------------------------------------------------

Removing the GIL *is* the obvious answer. The problem with this phrase is
the "just" part, not the "remove the GIL" part.

One of the key issues with threading models built on shared
non-transactional memory is that they are a broken approach to general
purpose concurrency. Armin Rigo has explained that far more eloquently
than I can in the introduction to his `Software Transactional Memory`_ work
for PyPy, but the general idea is that threading is to concurrency as the
Python 2 Unicode model is to text handling - it works great a lot of the
time, but if you make a mistake (which is inevitable in any non-trivial
program) the consequences are unpredictable (and often catastrophic from an
application stability point of view), and the resulting situations are
frequently a nightmare to debug.

The advantages of GIL-style coarse grained locking for the CPython
interpreter implementation are that it makes naively threaded code
more likely to run correctly, greatly simplifies the interpreter
implementation (thus increasing general reliability and ease of
porting to other platforms) and has almost zero overhead when
running in single-threaded mode for simple scripts or event driven
applications which don't need to interact with any synchronous APIs (as
the GIL is not initialised until the threading support is imported,
or initialised via the C API, the only overhead is a boolean
check to see if the GIL has been created).

The CPython development team have long had an essential list of requirements
that any major improvement to CPython's parallel execution support would be
expected to meet before it could be considered for incorporation into the
reference interpreter:

* must not substantially slow down single-threaded applications
* must not substantially increase latency times in IO bound applications
* threading support must remain optional to ease porting to platforms
  with no (or broken) threading primitives
* must minimise breakage of current end user Python code that implicitly
  relies on the coarse-grained locking provided by the GIL (I recommend
  consulting Armin's STM introduction on the challenges posed by this)
* must remain compatible with existing third party C extensions that rely
  on refcounting and the GIL (I recommend consulting with the cpyext
  and IronClad developers both on the difficulty of meeting this
  requirement, and the lack of interest many parts of the community have
  in any Python implementation that doesn't abide by it)
* must achieve all of these without reducing the number of supported
  platforms for CPython, or substantially increasing the difficulty of
  porting the CPython interpreter to a new platform (I recommend consulting
  with the JVM and CLR developers on the difficulty of producing and
  maintaining high performance cross platform threading primitives).

It is important to keep in mind that CPython already has a significant user
base (sufficient to see Python ranked by the IEEE as one of the top 5 programming
languages in the world), and it's necessarily the case that these users either
don't find the GIL to be an intolerable burden for their use cases, or else
find it to be a problem that is tolerably easy to work around.

Core development efforts in the concurrency and parallelism arena have thus
historically focused on better serving the needs of those users by providing
better primitives for easily distributing work across multiple
processes, and to perform multiple IO operations in parallel. Examples of this
approach include the initial incorporation of the :mod:`multiprocessing` module,
which aims to make it easy to migrate from threaded code to multiprocess code,
along with the addition of the :mod:`concurrent.futures` module in Python 3.2,
which aims to make it easy to take serial code and dispatch it to multiple
threads (for IO bound operations) or multiple processes (for CPU bound
operations), the :mod:`asyncio` module in Python 3.4 (which provides full
support for explicit asynchronous programming in the standard library) and
the introduction of the dedicated
`async/await syntax <https://www.python.org/dev/peps/pep-0492/>`__ for native
coroutines in Python 3.5.

For IO bound code (with no CPU bound threads present), or, equivalently, code
that invokes external libraries to perform calculations (as is the case for
most serious number crunching code, such as that using NumPy and/or Cython),
the GIL does place an additional constraint on the application, but one that
is acceptable in many cases: a single core must be able to handle all
Python execution on the machine, with other cores either left idle
(IO bound systems) or busy handling calculations (external library
invocations). If that is not the case, then multiple interpreter processes
will be needed, just as they are in the case of any CPU bound Python threads.


What are the key problems with fine-grained locking as an answer?
-----------------------------------------------------------------

For seriously parallel problems, a free threaded interpreter that uses
fine-grained locking to scale across multiple cores doesn't help all that
much, as it is desired to scale not only to multiple cores on a single machine,
but to multiple *machines*. As soon as a second machine enters the picture,
shared memory based concurrency can't help you: you need to use a concurrency
model (such as message passing or a shared datastore) that allows information
to be passed between processes, either on a single machine or on multiple
machines. (Folks that have this kind of problem to solve would be well advised
to investigate adopting
`Apache Spark <https://spark.apache.org/docs/latest/index.html>`__ as their
computational platform, either directly or through the
`Blaze <blaze.pydata.org/>`__ abstraction layer)

CPython also has another problem that limits the effectiveness of removing
the GIL by switching to fine-grained locking: we use a reference counting
garbage collector with cycle detection.
This hurts free threading in two major ways: firstly, any free threaded
solution that retains the reference counting GC will still need a global
lock that protects the integrity of the reference counts; secondly, switching
threads in the CPython runtime will mean updating the reference counts on a
whole new working set of objects, almost certainly blowing the CPU cache
and losing a bunch of the speed benefits gained from making more effective
use of multiple cores.

So for a truly free-threaded interpreter, the reference counting GC would
likely have to go as well, or be replaced with an allocation model that uses
a separate heap per thread by default, creating yet *another* compatibility
problem for C extensions.

These various factors all combine to explain why it's unlikely we'll ever see
CPython's coarse-graining locking model replaced by a fine-grained locking
model within the scope of the CPython project itself:

* a coarse-grained lock makes threaded code behave in a less surprising
  fashion
* a coarse-grained lock makes the implementation substantially simpler
* a coarse-grained lock imposes negligible overhead on the scripting use case
* fine-grained locking provides no benefits to single-threaded code (such as
  end user scripts)
* fine-grained locking may break end user code that implicitly relies on
  CPython's use of coarse grained locking
* fine-grained locking provides minimal benefits to event-based code
  that uses threads solely to provide asynchronous access to external
  synchronous interfaces (such as web applications using an event based
  framework like Twisted or gevent, or GUI applications using the GUI event
  loop)
* fine-grained locking provides minimal benefits to code that
  uses other languages like Cython, C or Fortran for the serious number
  crunching (as is common in the NumPy/SciPy community)
* fine-grained locking provides no substantial benefits to code that needs
  to scale to multiple machines, and thus cannot rely on shared memory for
  data exchange
* a refcounting GC doesn't really play well with fine-grained locking
  (primarily from the point of view of high contention on the lock that
  protects the integrity of the refcounts, but also the bad effects on
  caching when switching to different threads and writing to the refcount
  fields of a new working set of objects)
* increasing the complexity of the core interpreter implementation for any
  reason always poses risks to maintainability, reliability and portability

It isn't that a free threaded Python implementation isn't possible (Jython
and IronPython prove that), it's that free threaded virtual machines are
hard to write correctly in the first place and are harder to maintain once
implemented. For CPython specifically, any engineering effort directed towards
free threading support is engineering effort that isn't being directed
somewhere else. The current core development team don't consider
that a good trade-off when there are other far more interesting options still
to be explored.


What does the future look like for exploitation of multiple cores in Python?
----------------------------------------------------------------------------

For data processing workloads, Python users that would prefer something simpler
to deploy than Apache Spark, don't want to compile their own C extensions with
Cython, and have data which exceeds the capacity of NumPy's in-memory
calculation model on the systems they have access to, may wish to investigate
the `Dask <http://dask.pydata.org/>`__ project, which aims to offer the features
of core components of the Scientific Python ecosystem
(notably, NumPy and Pandas) in a form which is limited by the capacity of local
disk storage, rather than the capacity of local memory.

For CPython, Eric Snow has
`started working <https://mail.python.org/pipermail/python-ideas/2015-June/034177.html>`__
with Dr Sarah Mount (at the
`University of Wolverhamption <http://www.wlv.ac.uk/research/the-research-hub/the-doctoral-college/early-researcher-award-scheme-eras/eras-fellows-2014-15-/dr-sarah-mount/>`__)
to start seriously some speculative ideas I published a few years back
regarding the possibility of `refining CPython's subinterpreter
<http://www.curiousefficiency.org/posts/2012/07/volunteer-supported-free-threaded-cross.html>`__
concept to make it a first class language feature that offered true
in-process support for parallel exploitation of multiple cores in a way that
didn't break compatibility with C extension modules (at least,  not any more
than using subinterpreters in combination with extensions that call back into
Python from C created threads already breaks it).

For PyPy, Armin Rigo and others are actively pursuing research into the use of
`Software Transactional Memory`_ to allow event driven programs to be scaled
transparently across multiple CPU cores. I know he has some thoughts on how the
concepts he is exploring in PyPy could be translated back to CPython, but even
if that doesn't pan out, it's very easy to envision a future where CPython is
used for command line utilities (which are generally single threaded and often
so short running that the PyPy JIT never gets a chance to warm up) and embedded
systems, while PyPy takes over the execution of long running scripts and
applications, letting them run substantially faster and span multiple cores
without requiring any modifications to the Python code. Splitting the role of
the two VMs in that fashion would allow each to be optimised appropriately
rather than having to make trade-offs that attempt to balance the starkly
different needs of the various use cases.

I also expect we'll continue to add APIs and features designed to make it
easier to farm work out to other processes (for example, the new iteration
of the `pickle protocol`_ in Python 3.4 included the ability to
unpickle unbound methods by name, which allow them to be used with the
multiprocessing APIs).

Another potentially interesting project is `Trent Nelson's PyParallel work`_ on
using memory page locking to permit the creation of "shared nothing" worker
threads, that would permit the use of a more Rust-style memory model within
CPython without introducing a distinct subinterpreter based parallel execution
model.

Alex Gaynor also pointed out `some interesting research (PDF)
<http://researcher.watson.ibm.com/researcher/files/jp-ODAIRA/PPoPP2014_RubyGILHTM.pdf>`__
into replacing Ruby's Giant VM Lock (the equivalent to CPython's GIL in
CRuby, aka the Matz Ruby Interpreter) with appropriate use of Hardware
Transactional Memory, which may also prove relevant to CPython as HTM
capable hardware becomes more common. (However, note the difficulties that
the refcounting in MRI caused the researchers - CPython is likely to have
exactly the same problem, with a well established history of attempting to
eliminate and then emulate the refcounting causing major compatibility
problems with extension modules).

.. _Software Transactional Memory: http://pypy.readthedocs.org/en/latest/stm.html
.. _further tweaks: http://bugs.python.org/issue7946
.. _pickle protocol: http://www.python.org/dev/peps/pep-3154/
.. _Trent Nelson's pyparallel work: https://lwn.net/Articles/640178/
