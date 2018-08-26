#!/bin/bash
firefox --profile ~/.mozilla/firefox/m8xpc3im.presentation-mode -no-remote 'http://localhost:1948/integration-testing-with-splinter.md#/' &
reveal-md --disable-auto-open --highlight-theme vs integration-testing-with-splinter.md
