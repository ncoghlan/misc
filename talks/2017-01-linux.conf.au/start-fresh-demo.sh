#!/bin/sh
    rm /var/tmp/anitya-dev.sqlite
    python createdb.py
    python runserver.py &
    firefox --new-instance --profile ~/.mozilla/firefox/k6y5851o.release-monitoring-demo 'http://localhost:5000' &
