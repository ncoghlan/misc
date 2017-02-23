Shell window 1:

- not shown in demo
- Tab A: start reveal-md service
- Tab B: start Anitya service (see next section)

Local Anitya setup:

- not shown in demo, set up in background before starting talk

    vex anitya
    rm /var/tmp/anitya-dev.sqlite
    python createdb.py
    python runserver.py &
    firefox --new-instance --profile ~/.mozilla/firefox/k6y5851o.release-monitoring-demo 'http://localhost:5000' &

- log in to local Anitya instance with FAS

Shell window 2:

- shown in demo
- all tabs are in ~/fedoradevel/anitya
- all fedmsg commands are started *before* the talk commences
- Tab A: fedmsg-relay --config-filename fedmsg.d/fedmsg-config.py
- Tab B: fedmsg-tail --config fedmsg.d/fedmsg-config.py --no-validate --query topic
- Tab C: fedmsg-tail --config fedmsg.d/fedmsg-config.py --no-validate --really-pretty --topic org.fedoraproject.dev.anitya.project.map.new
- Tab D: fedmsg-tail --config fedmsg.d/fedmsg-config.py --no-validate --really-pretty --topic org.fedoraproject.dev.anitya.project.version.update
- Tab E: curl http://localhost:5000/api/by_ecosystem/pypi/requests

Demo steps:

(also included as speaker notes in presentation)

- Show Anitya web interface
- Show fedmsg info page
- Show the fedmsg-relay and first fedmsg-tail tabs
- Go back to web app and add Python requests module
- Show topics in first fedmsg-tail tab
- Show messages in topic-specific tabs
- Run curl command in final tab
