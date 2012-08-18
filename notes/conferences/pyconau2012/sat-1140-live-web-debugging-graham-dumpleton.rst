Debugging Live Python Web Applications
======================================

Graham Dumpleton (mod_wsgi author, New Relic)

Amjith (New Relic, will be presenting this at DjangoCon US0

(Many details missing - will link to slideshare once the slides are up)

Debugging
---------

Can't always duplicate problems in a devel environment

Debugging live servers can be dangerous
- crash the site
- corrupt data
- expose customer data

Tools to manage risk
- use software to restrict access
- script changes
- test beforehand

Passive monitoring
------------------

Safest approach

Needs to be set up in advance

Log file analysis tools

Capture Python exceptions (e.g. Sentry)

Monitor the server as whole

Application monitoring (this is what Graham does for a living at New Relic)
 (For open source custom equivalents, Graphite counters are a good option)

Web page performance analysis
- resource timing spec coming from W3C

Reaching the limit
------------------

Passive monitoring eventually gets to opaque blocks

Can add more monitoring hooks, *if* you can change the code

New Relic supports configuration and monkey patching at runtime, and
custom setups can do this, too.

Problem is you have to deploy a new build to make this happen

Thread Sampling and Profiling
-----------------------------

Full profiling is too slow for production

Periodic sampling can pick up big consumers of time

Targeted profiling can profile a function *sometimes* to minimise
overhead to the point of allowing it in production (just needs a
fairly simple decorator/context manager)

Still requires redeployment to gather more data

Browser tools
-------------

Can query a bit more, but still can't change the server

Interactive debuggers
---------------------

Can give full access, but can break the running application

New tool: ispyd
---------------

https://github.com/GrahamDumpleton/wsgi-shell
(originally wsgi only, hence the misnamed repo)

*Limited* access

Configure plugins to provide specific commands

Limits access (but you can enable the 'console' option for the Python plugin
if you want)

Can change configuration on the fly (e.g. New Relic plugin)

See the slides for more :)

This looks really cool with a lot of potential

Summary
-------

Monitoring is essential to detect the existence of problems, and to know where to start looking.

Create defined, controlled mechanisms to perform *detailed* queries for deeper dives into production problems that can't be reproduced in development

Hopes ispyd may catch on as a standard approaching for live debugging in a controlled manner (this is the first real public announcement)