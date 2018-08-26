#!/bin/bash
firefox --profile ~/.mozilla/firefox/m8xpc3im.presentation-mode -no-remote 'http://localhost:1948/controversial-peps.md#/' &
reveal-md --disable-auto-open --highlight-theme vs controversial-peps.md
