---
title: Integration Testing with Splinter
theme: beige
---

## Front-end<br/>Integration Testing
### with Splinter

Nick Coghlan (@ncoghlan_dev)

---

### What is splinter?

Note:

* splinter is a convenience wrapper around Selenium and related WebDriver
  backends for particular browsers
* I find it interesting because in combination with the BeautifulSoup HTML
  parsing library it makes front-end web UI testing almost as straightforward
  as backend API testing, and easy end-to-end integration testing makes me
  more willing to spend time learning to create my own user interfaces rather
  than relying solely on writing backend APIs and front-end CLIs

---

## Integration testing<br/>for backend APIs

Note:

* Before we get further into the front-end side of things though, I first want
  to talk about how we can handle end-to-end integration testing in general

---

### Behaviour Driven Development

Note:

* Behaviour Driven Development emphasises tests of user-visible system
  behaviour as a key tool in ensuring that software meets user expectations
* For systems driven by external needs, scenarios may be defined before the
  code is written in order to get preliminary agreement on the desired behaviour
* For systems driven by their developers' own needs, scenarios may be omitted
  originally and then defined later in order to capture pre-existing behaviour
  and reduce the risk of unintended behavioural changes

---

Desired behaviour is defined as scenarios:

    Given the following Python releases:
        | implementation | version | python_version | release_date
        | CPython        | 3.6.0   |                | 2016-12-23
        | CPython        | 3.6.2   |                | 2017-07-17
        | PyPy           | 5.8     | 2.7.13         | 2017-06-09
        | PyPy3          | 5.8     | 3.5.4          | 2017-06-09
     And a running instance of the backend service
    When I query the releases collection
    Then the reported HTTP status should be 200
     And all given releases should be reported

Note:

* As my running example, I'm going to use part of a side project I'm
  currently working on that will eventually track how long it takes for
  new Python releases to filter out through various distribution channels
* The piece of relevance today just stores & reports details about Python
  implementation release dates
* This scenario is a pretty typical example of a behavioural test case
* First, we start by defining the initial conditions in "Given" clauses - here,
  loading some example releases into the database and ensuring a local test
  server is running
* Then user actions and other events are specified as "When" clauses - here,
  querying a collection via the server API
* Finally the expected outcomes are specified as "Then" clauses - here, that
  the request succeeds, and returns the expected results
* Scenarios are designed to be readable, and even writable, by folks that
  wouldn't normally consider themselves to be programmers
* Showing it in action: "behave -i releases_api"

---

Individual steps are defined as code:

    @when('I query the {collection} collection')
    def query_api_collection(context, collection):
        collection_url = context._server_api_url + collection + "/"
        context._api_response = requests.get(collection_url)

Note:

* This shows a step definition using behave and the requests HTTP client
  library.
* behave is a BDD framework that relies on step definitions that each work
  with a shared context, writing to and reading from that context
* Here, we retrieve the backend API URL from the context, and store the API
  response back to it
* In behave, the mapping from the step text used in scenarios to the actual
  implementations of those steps is specified using decorators as shown
* For API testing, requests is almost always sufficient to handle the actual API
  access, perhaps with the aid of some suitable authentication libraries

---

Step parameters aren't limited to just text:

    @then("the reported HTTP status should be {expected_status:d}")
    def check_reported_http_status(context, expected_status):
        actual_status = context._api_response.status_code
        assert_that(actual_status, equal_to(expected_status))

Note:

* To check the HTTP status, we want to read the specific value used in the
  scenario as an integer
* behave provides native support for that using a format that's essentially
  the inverse of the str.format syntax
* the other piece shown here is that step definitions need a way to make
  *assertions* about the expected outcomes of a scenario
* while behave works with any library that throws AssertionError, the specific
  library shown here is pyhamcrest (imported as hamcrest)
* pyhamcrest is a test assertion library that allows us to declaratively define
  our expectations, and then use the "assert_that" command to check the actual
  live data against those expectations

---

Expectations can be set based on initial conditions:

    @then('all given releases should be reported')
    def check_for_expected_releases_in_api(context):
        data = context._api_response.json()["results"]
        assert_that(data, instance_of(list))
        for release in data: release.pop("url")
        expected = [has_entries(r) for r in context._given_releases]
        assert_that(len(data), equal_to(len(expected)))
        assert_that(data, contains_inanyorder(*expected))

Note:

* Here, rather than repeating the expectations in the test scenario, we
  instead get the data setup step to save what it loaded into the database
  as part of the scenario context
* That way, the expectation checking step can just check that what gets
  reported back matches what was loaded, reducing the number of places that
  need to be updated when new fields are added

---

### Collection of Step Definitions<br/>→ Step Catalog

Note:

* Taken together, all of the different scenario step definitions are referred
  to as the project's step catalog
* This provides a common vocabulary for describing the interesting initial
  states of the system (Given steps), interesting user actions and other
  external events (When steps), and the expected observable system behaviour
  (Then steps)

---

### Step Catalog + BDD Framework<br/>→ Scenario DSL

Note:

* Combing the project specific step catalog with the scenario definition
  syntax of the particular BDD framework in use then defines the domain
  specific scenario language available for testing that particular project

---

## Incorporating<br/>*browser-based*<br/>integration testing

Note:

* So that's the core concepts of integration testing covered, but where does
  GUI testing come into the picture?

---

### "I'm not a front-end developer"

Note:

* When it comes to software development, I personally prefer to focus on data
  pipelines and low level plumbing, where the main focus is on automated
  systems talking to each other, and the only humans directly interacting with
  things are the ones tasked with keeping that automation working
* At the same time, being able to put together at least a basic front end, and
  be confident not only that it's working as intended, but that it will *keep*
  working as intended is an incredibly useful skill to have

---

### Hence, splinter

Note:

* That means the reason I like splinter is because it makes end-to-end
  browser based integration tests feel almost as easy to write as the requests
  based API tests I'm more accustomed to developing
* There are plenty of other good reasons to like it, this is just the main
  reason why I personally became a fan almost as soon as I started using it :)

---

Defining a browser-based testing scenario:

    Given the following Python versions:
        | implementation | version | python_version | release_date
        | CPython        | 3.6.0   |                | 2016-12-23
        | CPython        | 3.6.2   |                | 2017-07-17
        | PyPy           | 5.8     | 2.7.13         | 2017-06-09
        | PyPy3          | 5.8     | 3.5.4          | 2017-06-09
     And a running instance of the backend service
    When I visit the Upstream Releases page
    Then the page title should be Python Upstream Releases
     And the given versions should be displayed

Note:

* Moving on to what this looks like in practice
* We get to reuse the existing setup step from our API testing
* We add a new entry to our step catalog that lets us visit app pages with
  our browser
* And also define new steps for checking the details of what actually happened

---

`splinter` now manages our front-end interactions:

    @when("I visit the {link_text} page")
    def visit_page_in_browser(context, page):
        context._browser = browser = splinter.Browser()
        browser.visit(context._base_url)
        browser.click_link_by_text(link_text)

Note:

* Where our API testing focused on a single request/response cycle, our browser
  testing focuses on a persistent browsing session, with `browser.visit()`
  becoming our direct counterpart to `requests.get()`
* starting up a full browser instance is a relatively slow operation, but
  splinter offers lots of options for avoiding that (such as sharing a single
  browser session between scenarios, and just clearing the saved cookies before
  each one, rather than starting with a completely fresh browser instance)
* splinter also offers lots of ways of finding things the way you'd advise a
  human to look for them in documentation (such as via the link text, or the
  contents of a message), rather than only offering invisible-to-humans
  criteria like CSS selectors or looking up by component ID (although it has
  those too)

---

And provides access to check the browser state:

    @then("the page title should be {expected_title}")
    def check_for_expected_page_title(context, expected_title):
        actual_title = context._browser.title
        assert_that(actual_title, equal_to(expected_title))

Note:

* Rather than having an API response to make assertions about, we instead
  have an open browser session where we can do things like check the
  current page title

---

The fully rendered HTML is available for inspection:

    @then("all given releases should be displayed")
    def check_displayed_releases(context):
        parser = bs4.BeautifulSoup(context._browser.html, "lxml")
        tbody = parser.find_all("tbody")[0]
        fields = "implementation", "version", "release_date", "kind"
        data = [{key: cell.get_text()
                    for key, cell in zip(fields, row.find_all("td"))}
                        for row in tbody.find_all("tr")]
        expected = [has_entries(r) for r in context._given_releases]
        assert_that(len(data), equal_to(len(expected)))
        assert_that(data, contains_inanyorder(*expected))

Note:

* The example project uses DataTables to dynamically render tables on the
  client, which means naive screen-scraping with requests or mechanize won't
  work (such clients are expected to use the JSON API instead)
* One of the key benefits of using a full-fledged browser for these test cases
  is that it means the client is running a full-fledged JavaScript engine
* As a result, the step definition needed to test the page in the web UI is
  only a few lines longer than that needed to test the JSON API
* Splinter even allows you to inspect the internal state of your frontend by
  allowing you to inject and run arbitrary JavaScript snippets. While I haven't
  personally needed that yet, it's nice to knows it's there if I want it.
* Showing it in action: run "behave -i releases_page"

---

## Tips<br/>&<br/>Tricks

Note:

* That's the end of the main front-end behavioural testing example, so in the
  remaining time I'll be going through a few different tips & tricks I picked
  up along the way

---

### Use requests for HTTP protocol testing

Note:

* Browsers are big complicated beasts where one page visit may trigger a
  multitude of distinct HTTP requests
* As a result, even though splinter provides a status_code attribute, the
  notion of a singular "HTTP status code" for a page visit is inherently
  somewhat ambiguous, and so splinter doesn't necessarily set it correctly
  when used with a local browser
* Accordingly, if you're wanting to test for particular HTTP status codes, or
  other similarly low level details (such as content headers), requests-based
  tests are likely to be both easier to write and faster to run

---

### Learning Selenium (etc) is still useful

Note:

* While splinter is a very nice abstraction layer, it *is* just an abstraction
  layer
* Just as the core concepts in requests come from HTTP, many of the concepts
  in splinter come from the underlying implementation layers, such as
  Selenium, WebDriver, HTML, and CSS
* This means that while splinter makes it possible to do things we might
  currently have no idea how to write ourselves, learning more about the
  underlying layers can be very helpful when trying to figure out why something
  isn't working as we might expect

---

### Use "xvfb" to run full browsers in CI

Note:

* CI environments don't offer actual attached monitors
* while drivers for headless browsers and direct-to-framework backends do
  exist, and can be useful as a form of unit testing, they miss the "test the
  system as it will be used in practice" aspect of integration testing
* X virtual frame buffers provide a useful way of pretending that a CI system
  has a monitor

---

### Be careful of race conditions

Note:

* When testing client-side rendering, there's an inherent race between
  the JavaScript engine actually updating the browser state and the test
  client checking for the expected state changes
* splinter exposes several APIs that support waiting for particular states
  with a timeout
* when those are insufficient, you'll want to roll your own timeouts using
  time.monotic()

---

### pytest-bdd & pytest-splinter

Note:

* due to the way behave executes step definitions, it doesn't integrate natively
  with pytest's rewriting of assert statements
* while it *is* possible to make that combination work if you have a specific
  need for it, doing so involves monkeypatching behave's step definition logic
* in most cases, folks that are already using pytest for their unit tests are
  likely to fare better with pytest-bdd and pytest-splinter if they want to
  implement any of the ideas discussed in this talk
* as far as I'm aware, the general concepts are the same, and it's mainly the
  way you write the individual steps that changes

---

### Q & A

Splinter: https://splinter.readthedocs.io

behave: https://pythonhosted.org/behave/

"Beginning BDD with Django" article series</br>
by Nicole Harris (Twitter: @nlhkabu)

https://github.com/ncoghlan/python-release-latency/

Note:

* Hopefully if you're like me, and historically averse to writing your own GUIs,
  I've convinced you that basic automated testing of front-end GUIs
  can be just as straightforward as testing backend APIs and front-end CLIs
* Even if you were already comfortable writing your own dynamic frontends,
  hopefully this offered you some ideas on how you might go about writing some
  automated tests for expected behaviour
* Questions?
