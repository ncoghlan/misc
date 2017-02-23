---
title: release-monitoring.org
theme: css/theme/league.css
---

## Drink from the firehose
### release-monitoring.org

Nick Coghlan (@ncoghlan_dev)

---

### Securing systems<br/>in a<br/>networked world

Note:

* Securing networked services is one of the most significant ongoing challenges
  in software development
* Enormous topic
* This talk is about one specific problem in that space

---

### OWASP Top 10 2013 A9:

Using components with known vulnerabilities

Note:

* Open Web Application Security Project
* Most of the issues relate to how the application itself
  is built and managed
* A9 is different: it's about how application developers
  and service operators manage their dependencies

---

### Update management<br/>is a key<br/>security concern

Note:

* I work on software supply chain management for Red Hat
* Update management spans the entire chain
* Publication, redistribution, and deployment

---

### Hardened bunkers
### Moving targets <!-- .element: class="fragment" -->
### Sitting ducks <!-- .element: class="fragment" -->

Note:

* Traditionally hardened bunkers - minimise attack surface, patch as needed
* Automation enables a new model - the moving target
* Regularly discard old instance and create new ones from scratch
* Eagerly upgrade to new versions of dependencies, design your testing and
  deployment systems accordingly
* If you don't do either? Sitting duck in a tin shed

---

### Linux in the<br/>hardened bunker era

Note:

* Linux distros were born at a time when publication meant posting a tarball
* Packagers took those tarballs and converted them to a more manageable format
* Automated testing was a luxury most upstream communities couldn't afford
* This meant regression and integration testing was left to commercial vendors,
  and the long term support model for Linux distributions was born
* Provides low risk security updates for a core set of critical components

---

### Times change

Note:

* Cost of running web services had dropped significantly in the past 10 years
* Many "free for open source projects" CI offerings available
* Quite common for projects to require tests to pass *before* merging changes
* Most modern language communities have a common publishing platform and format
* Improvements in automation make previously impractical things possible

---

### libraries.io

Developer-focused upstream monitoring

Launched: March 2015<!-- .element: class="fragment" -->

Projects monitored: ~2 million <!-- .element: class="fragment" -->

Publishing platforms monitored: ~33 <!-- .element: class="fragment" -->

Note:

* for example...
* open source project now backed by Brave New Software
* helps application developers be a moving target
* helps application developers find new projects of relevance to them
* tracks more than 2 million projects across 33 publishing platforms

---

### For comparison...

Ohloh/OpenHub: ~700k projects, since 2006 <!-- .element: class="fragment" -->

Freshmeat/Freecode: ~50k projects, 1997-2014 <!-- .element: class="fragment" -->

Debian GNU/Linux: ~50k projects, since 1993 <!-- .element: class="fragment" -->

Fedora GNU/Linux: ~20k projects, since 2003 <!-- .element: class="fragment" -->

Note:

* ~3 times as many projects listed as OpenHub in a fraction of the time
* 2 orders of magnitude more projects than even large Linux distributions
* upstream monitoring has historically been opt-in
* extra step for publishers or redistributors

---

### Linux in the<br/>moving target era

Note:

* Some use cases still call for carefully built hardened bunkers, so the
  familiar long term support model isn't going anywhere any time soon
* Majority of software is moving towards deploy-on-demand models, where updates
  are pushed out automatically, after going through automated regression testing
* Role of distros expands beyond *performing* QA activities specifically for the
  distro itself to also better enabling *automated* QA activities by end users

---

### release-monitoring.org

Redistributor-focused upstream monitoring

Note:

* maintains explicit mappings from upstream project names to downstream
  package names, as naming conventions can only get you so far
* aims to *systematically* automate the process of alerting redistributors to
  new upstream releases

---

### Show me the ~~code~~ service<br/>(Demo time!)

Note:

* running locally, as relying on real world events makes for a lousy demo :)
  - Show Anitya web interface
  - Show fedmsg info page
  - Show the fedmsg-relay and first fedmsg-tail tabs
  - Go back to web app and add Python requests module
  - Show topics in first fedmsg-tail tab
  - Show messages in topic-specific tabs
  - Run curl command in final tab


---

### Anitya

https://github.com/fedora-infra/anitya/

Note:

* Core web service that handles registration of upstream/downstream mappings
* Python application based on Flask and SQL Alchemy
* Currently still deployed on Python 2, but runs under Python 3
* Code lives under the fedora-infra group on GitHub: https://github.com/fedora-infra/anitya/

---

Anitya

### Upstream projects

Note:

* Original publishers of a piece of open source software
* Uniquely identified by home page URL
* Covers both open source libraries and full open source applications

---

Anitya

### Monitoring backends

Note:

* Plugins that can find and report new releases
* Lowest common denominator scrapes a web page with a custom regex

---

Anitya

### Upstream ecosystems

Note:

* Common project namespace with a default monitoring backend
* CPAN, RubyGems, PyPI, NPM, etc

---

Anitya

### Downstream distributions

Note:

* Redistributors of upstream projects
* Typically Linux distributions, but technically arbitrary

---

Anitya

### Upstream/downstream mappings

Note:

* Map upstream projects to their downstream counterparts

---

Anitya

### Event notifications

Note:

* Storing the upstream/downstream mapping is useful
* Also publishes asynchronous notifications via federated messaging

---

### fedmsg</br>(FEDerated MeSsaGing)

https://github.com/fedora-infra/fedmsg/

Note:

* ZeroMQ based brokerless messaging protocol
* Reference implementation in Python using twisted
* Originally short for Fedora Messaging, renamed after Debian also adopted it
* Code lives under the fedora-infra group on GitHub: https://github.com/fedora-infra/fedmsg/

---

fedmsg

### DNS based service discovery

e.g. "tcp://release-monitoring.org:9940"

Note:

* Endpoints located via DNS

---

fedmsg

### Reverse-DNS based topic namespaces

e.g. "org.fedoraproject.dev.anitya.project.version.update"

Note:

* Topics segmented by reverse DNS

---

fedmsg

### Message source authentication

Note:

* GPG or x.509 certificates
* validation can be switched off for local testing

---

fedmsg

### fedmsg-relay

Note:

* fedmsg is brokerless by design
* you never NEED to run a broker to use fedmsg
* brokers are nevertheless useful to manage message flow
* fedmsg-relay can provide a single public endpoint for
  listening to multiple event sources
* Anitya's dev config assumes a locally running relay

---

### Future enhancements

Note:

* While the service is already useful today, there's also plenty of scope for
  improvement
* in particular, it currently still mostly runs on the manual registration
  model

---

Future enhancements

### OpenID Connect

Note:

* Current programmatic API is read-only, with all operations to request
  project monitoring and adjust upstream/downstream mappings needing to go
  through the human-centric web interface
* Pending patch adds a Flask-RESTFul based API with OpenID Connect support,
  allowing these tasks to be more readily automated
* Initial patch just allows upstream project monitoring requests through the
  API, but other write APIs are expected to be added over time

---

Future enhancements

### Expanded public data set

Note:

* the requirement for manual registration has limited the number of projects
  added to release-monitoring.org so far
* with better programmatic APIs available, it becomes much easier to do things
  like scrape the contents of a distro repository and automatically register
  the appropriate mappings
* ensure all Fedora packages are covered
* incorporate Debian watch file data
* hopefully contributions from other distros

---

Future enhancements

### Add ecosystem details to public data set

Note:

* modelling ecosystems separately from monitoring backends is relatvely new
* release-monitoring.org historically allowed name duplication as long as
  the listed home page was different
* this proved to be a problem, as a given project may be listed under its
  actual home page, its VCS URL, its package index page, etc
* even HTTP vs HTTPS is enough to allow for duplicate entries
* populating the ecosystem details makes it possible to eliminate the
  duplication
* should be finished this week, at which point the by_ecosystem endpoint will
  work properly on the public service

---

Future enhancements

### libraries.io backend?

Note:

* Anitya currently includes its own backend plugins to monitor different
  language ecosystems for new releases
* it could be useful to develop a "meta-backend" that uses libraries.io for
  the release monitoring

---

Future enhancements

### Downstream version tracking?

Note:

* Anitya currently just tracks upstream releases and maps upstream project
  names to downstream package names
* A potentially interesting addition could be to also support tracking
  downstream *versions* of components
* It's not clear that it makes sense to do this in Anitya itself, though -
  it could easily be a separate service that uses Anitya's APIs to enable
  better data linking between upstream projects and downstream packages

---

### Q & A

https://release-monitoring.org

Anitya: https://github.com/fedora-infra/anitya/

fedmsg: https://github.com/fedora-infra/fedmsg/

Note:

* Hopefully I've convinced you that automated release monitoring is
  something we should collectively be doing
* There's plenty more to be done in getting more systematic about this,
  but libraries.io and release-monitoring.org offer a solid foundation
* Questions?
