Timelapser
==========

A quick and dirty Python project to capture timelapses of a window on Mac OS X

Captures a recording of one window using `screencapture`, gathering frames at a specified interval without a drop shadow or screen capture sound

Usage
-----

`python timelapser.py <APP_NAME> <INTERVAL_IN_SECS> <OUTPUT_DIR>`

Where
* APP_NAME is the name of the application you want to record
* INTERVAL_IN_SECS is the interval between frame captures, in seconds
* OUTPUT_DIR is an empty or nonexistant directory to store the frames

TODO
----

* General code cleaning and such
* Add a way to select a particular window instead of guessing that the first one is right
* Do the processing to make a video