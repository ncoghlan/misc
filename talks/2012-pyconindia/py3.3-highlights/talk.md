# Highlights of Python 3.3

----

# Who am I?

## Nick Coghlan (@ncoghlan_dev)

* CPython core developer since 2005
* Nominated member of the Python Software Foundation
* Red Hat toolsmith


----

# Unicode Size and Speed

* Unicode bytes-per-code-point now varies
* ASCII (or ASCII-escaped) and latin-1 text uses 1 byte per code point
* Most text will use 2 bytes per code point
* Will use 4 bytes per code point if needed
* Also a speed increase, due to reduced data copying
* Additional work optimising codecs (especially UTF-8 & UTF-16)

----

# Unicode Size (Demo)

<div id="pias-unicode-size-player" class="pias_player"></div>

----

# Other Unicode Updates

* ``u""`` literals are once again supported
* Unicode alias and named sequence lookup support
* Case folding method added: ``x.casefold()``
* Updated unicode database to 6.1
* ``\u`` and ``\U`` escapes are now permitted in ``str`` regexes

----

# Unicode Features (Demo)

<div id="pias-unicode-features-player" class="pias_player"></div>

----

# Error Reporting Enhancements

* Supressing display of exception context
* Better argument/parameter mismatch exceptions
* More useful hierarchy for OS interface errors
* Optional tracebacks for segfaults and stalled processes

----

# Import system enhancements

* Migrated to importlib - PEP 302 is finally Final!
* Import system is now defined in the language reference
* import statement, runpy, pkgutil now use same code
* Per-module import locks should reduce import lock contention
* Full namespace package support
* __init__.py files are now optional
* if no __init__.py, whole sys.path is searched for portions

----

# Integrated virtual environments

* ``pyvenv`` command, ``venv`` module
* ``pyvenv.cfg`` file identifies root dir of venv
* ``home`` key in config file identified base Python install
* behaves like virtualenv from ``user`` perspective

----

# Introspection improvements

* inspect.signature
* inspect.getclosurevars
* inspect.getgeneratorstate

----

# Data structure improvements

* More bytes/bytearray methods accept integers where appropriate
* collections.ChainMap added
* hash randomisation is enabled by default
* dict.setdefault() is now atomic
* dictionaries now share key state when possible
* types.MappingPrxoyType
* types.SimpleNamespace
* memoryview improvements

----

# Container ABCs

* collections.abc created
* range now supports equality checks (based on contents)
* list and bytearray now provide copy() and clear() methods

----

# IP address manipulation

* New ipaddress module
* Can define addresses, networks and interfaces
* IPv4 and IPv6
* Convert to string or integer to pass to socket APIs

----

Email policy framework

* Allows flexible control of email parsing rules
* Supports structured header processing
* 3.2 compatible by default
* Other policies offer stricter RFC compliance
* SMTP policy suitable for SMTP agents
* HTTP policy suitable for email serialisation

----

# Time improvements

* Better abstraction of platform differences in timers
* ``time.monotonic()`` for timeouts
* ``time.perf_counter()`` for benchmarking
* Improved access to platform specific timers

----

# Datetime improvements

* New timestamp() method for easy conversion to POSIX timestamp
* astimezone() argument is now optional, uses system TZ by default
* Invalid equality comparisons now return False instead of raising

----

# C accelerators

* decimal module now uses a C accelerator by default
* xml.etree C accelerator is now used by default

----

# IO enhancements

* 'x' mode for exclusive creation
* 'opener' parameter to more easily create custom IO stacks
* write_through option in TextIOWrapper to disable write caching
* flush keyword argument to print

----

# Compression algorithms

* new lzma module
* bz2 rewrite

----

# Filesystem manipulation

* os.replace API for cross-platform file replacement

----

# POSIX/Linux Features

* os.sendfile
* nanosecond timestamp support
* symlink handling support: ``follow_symlinks``
* symlink attack resistance: ``dirfd``
* And many more...

----

# Crypto Primitives

* hmac.compare_digest
* crypt.mksalt (Unix only)
* may have a cross-platform crypto primitive library in 3.4

----

# Socket & SSL improvements

* sendmsg/recvmsg/rcvmsginto
* 

----

# Dynamic context management

* contextlib.ExitStack
* covers contextlib.nested use cases that weren't handled by
  allowing multiple context managers in each with statement
* good for adapting between callback APIs and context management

----

# Delegating to a subgenerator

* yield from syntax
* gen.send() and gen.throw() passed to subgenerators
* expression result is retrieved from StopIteration
* generators are now allowed to return values

----

# Serialisation support

* Qualified names allows better serialisation of methods and nested classes
* Should be supported in new pickle protocol in 3.4
* Pickler objects now have a dispatch table 

----

# Q & A

Questions about 3.4 plans are fair game, too :)


Presentation tools:

* landslide: ``pip install landslide``
* playitagainsam: ``pip install playitagainsam``
* playitagainsam-js: https://github.com/rfk/playitagainsam-js/