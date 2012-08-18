PiCloud
=======

Amit Saha

http://echorand.me/2012/08/17/pyconau-2012-talk-on-picloud/

Intro
-----

Commercial cloud service

"Worker process" oriented rather than hosting oriented

20 core hours per month included in free account

Python API "import cloud"

REST API for more general access

Transfers dependencies automatically

Pre-initialised with NumPy/SciPy

Can tailor requested compute resources to a particular workload

Can run in a mode that uses multiprocessing locally rather than the cloud

Example
-------

``cloud.call`` is the most basic API!

Also the candidates you would expect, like ``cloud.call``

(problems with the video demo failing to display properly - sorted out
by using a different player)

(My comment: you could probably map a concurrent.futures executor to this API
pretty easily)

IPython notebook provided in repo for talk (see link above)

Other capabilities
------------------

Directed-acyclic graph of job dependencies (to pass data between jobs, map/reduce, etc)

Persistent data: cloud.files API to move data to/from the cloud and update it in jobs

More compex example: pyevolve
-----------------------------

Shows automatic deployment of dependencies

Identifies and pushes Python files that are referenced locally

Retrieves CSV files created pyevolve

Publishing APIs via REST
------------------------

Can designate a Python function to expose as a REST API

Environment
-----------

Automatic deployment only works for pure Python modules

Environments let you tailor what it is installed
- non-Python tools
- extension modules
- Ubuntu-based

Management APIs
---------------

Query job status, list jobs, etc.

Resources
---------

More links! (again, see link at top)

Q & A
-----

Any other services like this? (Don't know)

Security - SSH authentication

My Comments
-----------

Looks pretty interesting. Definitely aimed at the scientific crowd
rather than the webhosting crowd, thus the different emphasis and
"worker process" style API.


