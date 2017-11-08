#!/bin/bash
firefox --profile ~/.mozilla/firefox/m8xpc3im.presentation-mode -no-remote 'http://localhost:1948/getting-into-cpython-core-development.md#/' &
reveal-md --disable-auto-open --highlight-theme vs getting-into-cpython-core-development.md
