# The Rise of<br/>Multilingual<br/>Programming

---

# Make all strings<br/>be Unicode<br/>(PEP 3000, 2004)

# Presenter Notes

* These five little words have had a profound impact on me
* I've been a CPython core developer since 2005
* Those five words are from the original PEP 3000, since moved to PEP 3100,
  the place where the core developers accumulated all the non-controversial
  Python 3 design changes
* Guido started the Python 3 project in earnest in 2006, with Python 3.0
  released in 2008
* Seven years later, we're still dealing with some of the consequences

---

# Why change<br/>the default?

---

# [Demo: Python 2<br/>Data Analysis]

# Presenter Notes

* Python 2 defaults to only handling English text
* Can handle some non-English text format in some usage models
* Some aspects (like identifiers) are entirely restricted to English
* This causes problems for data driven programming tools like Pandas
* Folks should also be able to learn to program without learning English first
* This default isn't OK for a language commonly used to teach programming

---

# One small part of a much larger pattern

# Presenter Notes

* This reflects a core principle guiding the evolution of computing
* Making them better at communicating with and between humans
* We actually started on the "communicating between humans" problem long
  before modern programmable computers were invented
* The legacy of this history remains with us to this day

----

# The long shadow of the telegraph

# Presenter Notes

* Some aspects of Unicode actually date back to the invention of Baudot code
  almost 150 years ago
* the teletypes used to send telegraph messages are the origin of the "tty"
  abbreviation in Unix and Unix-derived systems
* Baudot's code was adopted with some changes by Western Union in 1901
* standardised as ITA2 in 1930

----

# <img src="ita2.png" height="392" width="684"/>

# Presenter Notes

* Image from https://commons.wikimedia.org/wiki/File:Ita2.png
* 5-bit modal encoding, switching between Letters and Figures
* still in use today for especially low bandwidth channels
  (using 8 bits per character rather than 5 adds 60% overhead!)
* NUL, CR, LF, and BEL appear
* space was considered a control character rather than text
* Russian derivative MKL-2 adds a third mode for Cyrillic characters
* modal encodings cause problems, as missing a shift character garbles the
  rest of the message

----

# (7-bit) ASCII

# Presenter Notes

* By the early 1960s, American developers wanted room for more characters
* Created the American Standard Code for Information Interchange
* Avoids the problem with modal encodings, where missing a single shift
  character can corrupt the rest of the stream
* Also considered eight bits to allow the use of binary coded decimal,
  but decided to save a bit for efficiency
* Transmission channels were still slow enough back then that the 14%
  overhead of the extra bit was considered too high

----

# <img src="ascii.png"/>

# Presenter Notes

* Image from https://en.wikipedia.org/wiki/File:ASCII_Code_Chart-Quick_ref_card.png
* Can see the ITA2 control characters have been preserved
* The pound currency symbol in ITA2 is replaced by the dollar sign in ASCII
* Some details of the layout relate to handling the consequences of high
  bit error rates in unreliable transmission channels
* Others relate to making particular operations involve only checking or
  flipping one or two bits

----

# Extended ASCII

# Presenter Notes

* ASCII is great if you speak English, not so great otherwise
* Various extended ASCII formats added other letters
* Worked reasonably for European and Cyrillic languages
* Less well for Asian languages

----

# A cornucopia<br/>of codecs

# Presenter Notes

* If you want to find popular ASCII incompatible codecs, look to Asia
* Shift-JIS, Big5, ISO-2022
* Hye-Shik Chang's CJK codecs were included in Python 2.4 in 2005
* Python standard library now supports almost 100 language codecs
* Problem solved, right?

----

# Bilingual<br/>computing

# Presenter Notes

* Language specific encodings made computers bilingual
* English and the language the codec was designed to support
* This works OK if computers never talk to each other
* Problematic for networked computers and portable media
* Also problematic for tasks like translating between languages

----

# Multilingual<br/>computing

# Presenter Notes

* What we really wanted was "any language, any time"
* More accurately, "all languages, all the time"
* A way of representing any human language in the world
* With a transition plan from ASCII based infrastructure

----

# ⓊⓃⒾⒸⓄⒹⒺ

# Presenter Notes

* And so we come to Unicode
* Unicode was invented in the early 90's by engineers from Apple and Xerox
* Initial attempt was 16-bit only
* Left out a lot of kanji and han characters needed for names
* Later expanded to 21 bits, using up to 32 bits for storage
* Problem solved now, right?

----

# UTF-8<br/>UTF-16-LE<br/>UTF-32

# Presenter Notes

* No, problem not completely solved
* Even the rise of Unicode hasn't ended the codec wars
* Choosing in-memory, on disk and wire protocol encodings has trade-offs
* These three universal codecs cover most use cases

----

# ASCII<br/>compatibility<br/>(UTF-8)

# Presenter Notes

* Single bytes for ASCII code points, up to 4 bytes for other code points
* Key advantage of UTF-8 is that it is ASCII compatible
* Also most efficient for ASCII heavy data, like many network protocols
* Became the most popular encoding for public HTML sites in 2008
* Preferred local encoding on POSIX systems, including Mac OS X
* In the mobile world, we see it in iOS and native mode in Android

----

# Basic<br/>multilingual plane<br/>(UTF-16-LE)

# Presenter Notes

* The original 16-bit Unicode is now called the basic multilingual plane
* Includes almost all commonly used characters in modern languages
* This encoding uses 2 bytes for the BMP, 4 bytes otherwise
* Can be more efficient than UTF-8 for non-English texts
* Preferred local encoding on Windows, the .NET CLR, the JVM
* Also seen in the Dalvik and ART runtime on Android

----

# O(1) random<br/>code point access<br/>(UTF-32)

# Presenter Notes

* Computers are still really good at processing regular arrays
* Both UTF-8 and UTF-16-LE are variable width encodings
* Simple array oriented algorithms become error prone
* Can be worth taking the memory hit to simplify processing algorithms
* This is what Python does to share algorithms between binary & text data

----

# Where does<br/>Python 3 stand?

---

# [Demo: Python 3<br/>Data Analysis]

# Presenter Notes

* Far more opinionated than Python 2 on the right way to handle text data
* User space processing is largely in a good place
* Python 3.5 restores binary data interpolation

----

# System boundaries:<br/>Mac OS X

# Presenter Notes

* First OS to enforce UTF-8 as the default system encoding
* CPython hardcodes this rather than detecting it
* I'm not aware of any major remaining issues
* Not that surprising, given Apple have been working on Unicode support longer
  than anyone else

----

# System boundaries:<br/>Windows

# Presenter Notes

* CPython still uses some 8-bit APIs on Windows for standard streams
* win_unicode_console project on PyPI can help
* bundled libraries like OpenSSL can also sometimes make things interesting

----

# System boundaries:<br/>Linux & other POSIX based platform

# Presenter Notes

* Doesn't cope well with bad encoding advice from POSIX environments
* systemd sets it reliably, other Linux init systems less so
* still working on getting glibc to offer C.UTF-8 by default
* I don't know how reliable other POSIX based platforms are in supplying
  correct encoding settings

----

# Q & A<br/><br/>@ncoghlan_dev
