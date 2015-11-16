Embedding PIAS players in Landslide:

ALAS, this isn't currently working with Unicode in the output...

===================

Disable resource embedding when generating the HTML (it confuses PIAS)

===================

Apply theme/slides.js.patch to theme/js/slides.js

===================

Add PIAS recordings to demo-js directory as "demo-name.js"

===================

Add demo slides as:

---

# Demo heading

<div id="pias-demo-name-player" class="pias_player"></div>

---



