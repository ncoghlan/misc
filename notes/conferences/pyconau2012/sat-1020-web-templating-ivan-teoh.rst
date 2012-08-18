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

Diazo and XSLT
--------------

Mako
----
