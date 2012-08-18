Virtual Robotic Cars
====================

Tennessee Leuwenburg (sp?)

Why?
----

Loves robotics as an intellectual playspace

Submitted the talk partly as a motivation/excuse to spend more time playing


Real World
----------

Brief history of auto racing

Many current "self-driving car" efforts

DARPA Grand Challenge video

Urban Grand Challenge video ($40k radar array!)

Traxxas X01 (video)
- 100 MPH remote control car
- controlled via iPhone

Range of technology
- drive-by-wire(less)
- remote drive-by-wire(less)
- supervised autonomous (ABS, 
- fully autonomous

Few real world races
- DARPA Grand Challenge
- DARPA Urban Challenge
- Audi Pikes Peak

Virtual World
-------------

TORCS - The Open Racing Car Simulator

TORCS video

Something anyone can do

Similar abstractions to a real robotic car
- distance and other sensors
- speed, steering, braking controls
- noisy sensors
- complex environments
- open-ended design and problem definitions

Can go as far as you want in learning

Yearly TORCS competition
- current entries Java & C++

Now has Python bindings, so can write car control
systems in Python

pyScrcClient - uses a socket to talk to the TORCS server

Udacity course - programming a robotic car in 7 weeks

The TORCS Vehicles
------------------

Sensors
- 20 range-finders
- current angle to track bearing

Controls
- accelerator
- brake
- gear changes

Trigonometry to get from distance sensors to an actual picture of the world

Getting Started
---------------

Just follow the track center line!

Beyond that
- steering and path planning
- acceleration and braking
- collision avoidance (for racing)
- strategy (beyond the scope of the talk)

No compass sensor, so first step is to build a motion model for the car
itself

TORCS updates every 0.02 seconds

Places an upper limit on your processing time

Evil maths!
-----------

More trig to work out the expected centre point of a turn.

Simplify the model of the car to a bicycle rather than worrying about the
four wheels

How to model:
    - assume you know the car positionss
    - see what happens
    - draw something so you can see what your car is "seeing"

Yakkety Sax goes with everything!

(Oops, wrong version of the slides, opened right version to get correct
embedded video)

Localisation
------------

Given a map, use it work out where you are

Feedback loop between deriving the map from sensors, and using the results
of your sensors to determine where you are


Local vs Global planning
------------------------

Global: mapping + localisation

Local: collision avoidance, ABS, etc

SLAM and Filtering
------------------

Can use "mapping runs" to build up hypothesis maps

Can use track distances to filter particles after a complete lap
(known location)

Great free resources online

Virtual Robotic Car Racing lets you explore and exploit most of the
related algorithms

Resources
---------

See slides for links (I'll add a link to the slides once they're up)

Q & A
-----

(missed the first couple)

Polulu - remote control chassis with reversible wheels and an Arduino
built in to embody your questions

Can download and run bots from the competition to see how good (or bad)
you are.

No GPS in the sim software, so you can't "pre-plan" too much (and competition
uses novel tracks)

No accelerometer info in TORCS (which seems odd, since this is the first
sensor you would add to a real version)

Strategy depth is immense! (e.g. blocking lines to prevent following cars
using them)

My Thoughts
-----------

Sounds like an interesting way to explore various AI topics.
