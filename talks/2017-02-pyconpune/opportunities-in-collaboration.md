---
title: Opportunities in Open Collaboration
theme: white
---


## Opportunities and challenges
## in open collaboration

Nick Coghlan (@ncoghlan_dev)

---

### This is weird

Note:

* Think for a moment about how weird this is
* I am an Australian
* Giving a presentation in India
* About a programming language invented in the Netherlands
* Named after a British sketch comedy group
* and legally backed by an American public interest charity

---

### This is cool

Note:

* For all our cultural differences
* And for all the complications of history and global politics
* We can at least agree on the fact we like solving problems with Python
* And that we all collectively benefit when we work together to improve it

---

### This is fascinating

Note:

* I am not an anthropologist
* I am not an economist
* I am not a political scientist
* But I am an open source practitioner with a vested interest in the
  sustainability and growth of open source ecosystems in general, and the
  Python ecosystem in particular
* And that means paying attention to how open collaboration models intersect
  with other social, financial, and political systems

---

### Open collaboration<br/>creates<br/>global opportunities

Note:

* At least in principle, collaborating online should make our
  systems and processes accessible to anyone with an internet connection

---

### Opportunities<br/>are not<br/>outcomes

Note:

* Unfortunately, reality is more complicated
* Just because an opportunity exists doesn't mean people are going to be
  in a position to take advantage of it

---

### Constraints on<br/>open collaboration

Note:

* In practice, there are a lot of external factors influencing who chooses
  to participate in our communities
* Not only who attempts to participate at all, but also who stays and continues
  to participate over time

---

### Interest: why collaborate?
### Ability: how can I contribute?

Note:

* Interest & ability are two key factors that most folks intuitively
  recognise as being important
* If you ask participants in a lot of open communities, they will tell you that
  everyone with the relevant interest & ability is already there
* If people aren't participating, then they're assumed to lack either interest
  or relevant abilities
* People will often say this even if their contributor community is entirely
  unrepresentative of their user community, let alone the world at large
* If you hear the phrase "It's a pipeline problem", then this is almost
  certainly the mindset being used to approach the question of skewed
  demographics

---

### Access: where do we collaborate?

Note:

* Digging a little deeper though, we find there are some other major factors
  influencing participation in collaborative communities
* Access refers to specific tooling choices around communication, language
  barriers, time zone barriers, and opportunities for offline collaboration
* A common problem with single vendor commercially sponsored open source is
  cases where only people working for the sponsoring company can really
  participate fully in decision making processes


---

### Time: when do we collaborate?

Note:

* For any volunteer community, the availability of free time, and a willingness
  to invest it in that particular community, is always going to be a key
  constraint
* Especially a challenge when mixing paid full-time professionals with casual
  volunteers

---

### Energy: how do we collaborate?

Note:

* Energy refers to the fact that when contributors are having to invest
  emotional energy into defending their right to be actively involved in that
  community, they're less likely to remain engaged
* While I didn't come up with the phrase, an apt summary of these additional
  challenges is to describe the pipeline as being leaky and full of acid


---

### Sustaining<br/>collaborative<br/>communities

Note:

* So what can we do?
* Left to their own devices, a growing collaborative community is a recipe for
  maintainer frustration and burnout as the demands of the task begin to exceed
  their available time
* At the same time, it isn't reasonable to expect volunteers to be willing to
  switch from treating their personal side project as a hobby to treating it as
  an unpaid second job

---

<img class="plain"  src="images/contributors-etc.svg"/>

Note:

* One scaling model that has been found to work better than anything else we've
  tried so far is to have a mix of volunteer contributors and paid participants,
  with the project structured to ensure that influence over the project
  direction is shared between the two groups
* Different folks care about different things, and have varying amounts of
  time to devote to particular areas
* Contributors, colleagues, clients, and customers - four very
  different ways of directly or indirectly engaging with open
  collaborative communities
* Not an immediate or simple fix, but has the key benefit of introducing
  institutions to the system that can be encouraged to invest actively in
  improving community management practices

---

### Contributors:<br/>Changing the world<br/>(as a hobby)

Note:

* The key distinction I make between contributors and colleagues in
  open source, is that contributors are offered the opportunity to have
  an impact, but have no specific responsibilities
* Projects have the authority to decline to accept attempted contributions,
  and to define the criteria for inclusion, but whether or not the pay-off
  in personal experience and impact on the project for meeting those criteria
  is worth the time invested is a question left to each individual contributor
* Students, academics, established industry professionals, retirees, and folks
  that simply enjoy tinkering with code are great candidates for getting
  involved in open source as volunteer contributors

---

### Not their circus,<br/>not their monkeys

Note:

* "Not my circus, not my monkeys" is a wonderful Polish saying for disclaiming
  responsibility for resolving a problem
* When asking contributors to spend time on something, it's essential to
  remember the principle of "no obligation without compensation"
* The only real obligation for individual contributors is to respect community
  codes of conduct - when we don't want to do that, we have the entire rest of
  the internet to play in

---

### Colleagues:<br/>Changing the world<br/>(as a job)

Note:

* Once folks accumulate responsibilities in a community, the time commitments
  start to grow, and sustainability requires finding ways to get paid for the
  work
* Important to care about the sustainability of our peers' community
  involvement, and support folks in managing their stress levels
* Colleagues in this sense may not be employees of the same company - they may
  work for trade associations, non-profit foundations, competing
  redistributors, companies that are running self-supported instances
  of the project, consulting companies that rely on the project, and more


---

### Clients:<br/>Solving specific problems

Note:

* To make money in open source, key question is not "what do you want to build?"
* Rather: Whose problems are you planning to solve? Why should they trust you
  to solve them?
* Most obvious form: open source based software consulting businesses
* A second form: organisations running self-supported open source software
* A third form: philanthropic grants

---

### Customers:<br/>Meeting a<br/>common need

Note:

* Funding based on specific clients or benefactors can work well at
  a smaller scale, but struggles to create the kind of recurring funding
  needed to sustain hundreds or thousands of people working on open source
  projects
* Key business development task is figuring out what folks are ready, willing
  and able to pay for that you're prepared to invest time and money in
  delivering
* While my own experience with this is in the context of commercial clients
  and customers (both from the customer perspective and the redistributor
  perspective), there are also examples of it working well with non-profit
  organisations (consider MediaWiki, Wikipedia and the Wikimedia Foundation,
  or Mozilla and Firefox)

---

### Aligning incentives<br/>and<br/>sustaining participation

Note:

* While it's by no means assured, this kind of institutional involvement
  can make for a much healthier and more enjoyable collaborative community
* For the final part of this talk, I'm going to run through some examples
  of how this model can help us get the outcomes we'd like from the
  opportunities that open collaboration models create

---

### Interest:
### Solving our own problems

Note:

* The most common motivation for getting involved as a contributor is having
  a particular problem that we want solved, such as a specific bug we want
  fixed, or a new feature that we really wish was available by default
* In a healthy collaborative ecosystem, opportunities exist for clients and
  customers that choose to do so to become contributors representing their
  own interests directly

---

### Example:<br/>contextlib.ExitStack

Note:

* The original version of the contextlib module included a "nested()"
  context manager that turned out to encourage resource leaks
* As a result, we removed it when syntactic support for nested context
  managers was added
* However, I still wanted a way to dynamically manage context managers,
  so I kept iterating on ideas in contextlib2 until I settled on the API
  design that became contextlib.ExitStack
* This is the area where I think institutional involvement makes the least
  difference, except insofar as it brings more users to the project who then
  become potential contributors

---

### Interest:
### Helping to solve<br/>other people's problems

Note:

* For folks specifically paid to participate in collaborative communities,
  the goal is generally to meet the needs of their employer, or their
  employer's customers, rather than to pursue their own interests
* Even for volunteer contributors, their goal may be to meet the needs of a
  particular user community that they value for their own reasons (for example,
  many Pythonistas volunteer to help out folks using Python for education and
  for scientific research)
* A solid base of funded contributors can also help faciliate the contribution
  and collaboration process for other contributors

---

### Example:<br/>Python 3.6 secrets module

Note:

* One of the ongoing challenges with newcomers to Python is teaching them
  that the random module is designed for simulations and games where
  unguessable randomness isn't required, and hence it shouldn't be used for
  security-sensitive purposes
* instead folks have historically been directed to a variety of one-line
  recipes that implement the particular behaviour they need
* this generally hasn't worked very well, so the new secrets module groups
  together a collection of those recipes as a named standard library module,
  in the hope that "use the secrets module" will become the obvious (and
  correct!) answer to generating security sensitive random values in Python

---

### Interest:
### Having someone else<br/>solve our problems

Note:

* Sometimes we have money available to invest in solving a problem, but only
  limited availability of our own time, or that of our peers in an organisation
* In these cases, organisations have a lot of opportunities to invest in
  supporting open source projects and tailoring them to their needs either
  by hiring open source developers specifically to work on the relevant
  upstream projects, or else by working with open source vendors that invest
  appropriately in sustaining their upstream communities

---

### Example:<br/>long term support contracts

Note:

* Institutional open source users regularly want to run open source components
  for longer than the upstream community are willing to support them
* It can be reasonable to do this, but you need to invest in watching the
  upstream project closely for security problems, and backport any relevant fixes
* That involves a significant time commitment and isn't inherently rewarding
  enough to attract volunteer efforts, so it's a common service for commercial
  redistributors to offer to their clients and customers

---

### Ability:
### Collaboration is about<br/>more than code

Note:

* In open source communities, we have a tendency to treat the source code as
  the only essential element
* In the early days of open source, this was even arguably true - having an
  open source option available at all was sufficiently rare that there wasn't
  much opportunity for potential users to be choosy
* Times change though, and we're now counting the number of available open
  source components in millions rather than thousands or tens of thousands
* In that context, design, documentation, quality assurance, and effective
  community management have a major influence on project adoption and impact

---

### Example:<br/>organising community events

Note:

* Events like this one aren't possible without the signficant number of
  volunteers that contribute to making them happen
* In addition to sponsoring these events directly, organisations
  engaged with the relevant communities also often allow the use of work time
  both to attend the event, and to participate in organising it
* They may also offer meeting spaces to organisers in the lead-up to events,
  and sometimes even participate in hosting the event itself
* Many Python community meetups and workshops are also hosted in the offices of
  local organisations that use Python

---

### Access:
### Helping people<br/>meet in person

Note:

* One situation that poses significant challenges is the degree to which
  meeting in person can accelerate the process of establishing trust at a
  personal level, and hence gaining additional influence in a community
* the fact we're more willing to trust people we've actually met isn't something
  we can readily alter - it's an inherent part of being human


---

### Examples:<br/>Conference financial aid<br/>Regional conferences

Note:

* Financial aid and scholarship programs aim to reduce the cost of travel and
  accommodations as a barrier to participating in major community events
* The growing number of regional Python community events also help build
  connections within and between communities more effectively, rather than
  attempting to grow the original PyCon indefinitely
* Folks getting to attend events as employer funded business trips can also
  make a significant difference


---

### Access:
### English as a pre-requisite

Note:

* Not a lot we can do about this in the context of open source projects
  with established default languages for collaboration (e.g. English for Python,
  Japanese for core Ruby)
* translated documentation and localised applications can make a big
  difference at an individual project level
* local community workshops, user groups and regional conferences can help
  avoid requiring English up front, even if it will still be useful later
* but institutions can also structure themselves to help mitigate this problem

---

### Example:<br/>making the PSF more distributed

Note:

* English is well-established as the default language used to interact with the
  Python Software Foundation and that's unlikely to change
* however, the charter for the PSF Grants Working Group explicitly calls out
  6 different regions of the globe that must have at least one member each
* the PSF are also currently continuing to trial a more scalable Ambassador
  program in South America
* with any luck, that program may eventually give more folks around the world
  the opportunity to collaborate with official representatives of the PSF in
  their native language, with the Ambassadors handling the translation to
  English

---

### Time:
### Summarising complex discussions

Note:

* Just keeping up with complex design discussions on project mailing lists
  can be incredibly time consuming
* Institutions like Linux Weekly News, and vendor blogs can summarise these
  discussions in a way that makes things easier to follow for less engaged
  observers
* Communities can also incorporate this activity as an explicit part of their
  structured decision making processes


---

### Example:<br/>Python Enhancement Proposals

Note:

* One of the key purposes of the Python Enhancement Proposal process is to
  allow discussion participants to just follow and respond to PEP updates,
  rather than having to read every single related mailing list message
* These persistent summaries also make it easier for new contributors to get
  up to speed on the history of particular design decisions

---


### Time:
### Funded collaboration<br/>opportunities

Note:

* Open source isn't developed by magic internet pixies, so contributors
  still need to eat, and still need somewhere to sleep
* So in addition to full-time employment, part-time employment and paid
  internships working on open source projects, institutions can invest
  in supporting upstream communities in other ways


---

### Examples:<br/>Outreachy<br/>Google Summer of Code<br/>Mozilla Open Source Support

Note:

* Some particularly interesting examples are:
* Outreachy, now run by Software Freedom Conservancy, which offers paid
  open source internships to members of groups that are broadly underrepresented
  in open source communities
* Google Summer of Code, which introduces large numbers of students to open
  source and open collaboration every year
* Mozilla Open Source Support, which is a general grants program for existing
  open source projects which could use an additional financial boost to achieve
  particular goals


---


### Energy:
### Encouraging more inclusive<br/>collaboration

Note:

* When the goal is to diversify a previously relatively homogenous group,
  it generally isn't sufficient to just say "We welcome anyone"
* Instead, it's necessary to make a convincing case to people that you're not
  just looking for token participation to tick a "There, we have diversity now"
  box, and are instead genuinely looking to expand the scope of participation
  in that community
* Explicitly documenting expected standards of behaviour in the form of Codes
  of Conduct is a beneficial step in that process, but it's far from being
  sufficient on its own


---

### Example:<br/>PyLadies<br/>DjangoGirls

Note:

* PyLadies was founded in 2011 in Los Angeles, and has since expanded to have
  more than 60 chapters around the world
* DjangoGirls was founded in 2014, and has since hosted workshops in 68
  different countries, and more than 200 hundred different cities, reaching
  thousands of women around the world
* the impact of these and other efforts can be seen in the changing demographics
  of speaker line-ups and event attendance, where we're starting to see things
  become far more balanced than they once were (although there's also clearly
  still a long way to go)

---


### Energy:
### Formally acknowledging<br/>community contributions

Note:

* While it may sound like a small thing, it can make a surprisingly big
  difference when organisations say to volunteers "We recognise your
  contributions, and we appreciate them"
* One of the most sincere forms of acknowledgement can be a job offer or a
  promotion, but there's also a lot of other things that organisations can
  do to acknowledge the efforts of volunteer contributors

---

### Example:<br/>PSF Community Service Awards

Note:

* The PSF's Community Service Awards are granted on a quarterly basis to
  recipients that the Board acknowledges as having performed a significant
  service or services on behalf of the wider community
* Since 2008, more than 60 awards have been made, for contributions ranging
  from maintaining the PSFs collaboration infrastructure, to organising and
  supporting community conferences, to developing key promotional material
  for the community in the form of the PSF brochure, coordinating the PSF's
  participation in the BBC micro:bit project and curating the large collection
  of Python conference videos maintained at pyvideo.org

---

### Improved outcomes mean<br/>even more opportunities

Note:

* One of the most interesting aspects of more expansive communities is that
  they offer ever more avenues for us to explore at a personal level
* Honza covered some of his own career journey yesterday
* For myself, open source has allowed me to make the jump from embedded signal
  processing development to supply chain management tools for the world's
  largest open source company
* I've also had opportunities to meet and help educators, scientists, and other
  folks around the world that I never would have encountered otherwise
* My own hope is that our community will continue learning and growing, and
  finding ever more opportunities to help each other improve


---

### Questions?

Note:

* Don't forget the resource slide if people ask :)

---

### Resources:

* https://opensource.com/resources
* https://opensource.guide/
* http://producingoss.com/
* https://modelviewculture.com/issues/open-source

Note:

* This is just one way of framing the opportunities and challenges involved
  in participating in collaborative communities
* These links go into a lot more detail on some of these topics, and many
  more besides
