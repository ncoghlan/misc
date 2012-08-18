Web Templating Battle
=====================

Ivan Teoh (PretaWeb - government CMS provider)

Comparing 5 Python web templating systems


Intro
-----

Web templates - separating presentation from content

5 to be reviewed:

- Django
- Chameleon
- Jinja2
- Diazo and XSLT
- Mako

Django templating
-----------------

Text based

Customisation in Python code

Separate variable interpolation syntax (``{{``, ``}}``) and tag syntax
(``{%``, ``%}``)

Also have filters etc

Django-specific

Chameleon
---------

HTML/XML based

Compiles to Python bytecode

Language is "page templates", originally from Zope

Python is the default expression langage

Used with Pyramid, Zope, Plone, Grok, standalone

Commands embedded into HTML attributes. Also allows arbitrary Python
snippets in 2.0

Jinja2
------

text based (syntax very similar to Django templates)

compiles down to Python bytecode


Diazo and XSLT
--------------

XML rules files

Combines web designer template with developer backend

Uses CSS classes and XSLT to drive the transforms

Various directives identify the pieces (e.g. identifying the theme file)

No looping constructs, just use XSLT

From Plone 4.2 (this came up in the Q&A)

Mako
----

Embeds Python directly in the template (i.e. Python server pages)

Uses ``<%``, ``%>`` to identify code blocks


Summary
-------

No real battle, no real winner

Driven by different use cases & history

Q & A
-----

5 chosen are under active development

Diazo seemed very complicated relative to others. Designed to support a
drag-and-drop theme designer for use by CMS clients. Still a little
complicated to use from the developer side to set it up.

My Thoughts
-----------

Reasonable overview, but hard to get into any detail in 25 minutes.

Would have been nice to have explicit pros/cons for each one.
