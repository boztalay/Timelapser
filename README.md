Timelapser
==========

A quick and dirty Python project to capture timelapses of a window on Mac OS X

Captures a recording of one window using `screencapture`, gathering frames at a specified interval without a drop shadow or screen capture sound

Note that this doesn't make any efforts to compress the output (it's gonna get big), and expects the interval between frames to be at least one second

Usage
-----

`python timelapser.py <APP_NAME> <INTERVAL_IN_SECS> <OUTPUT_DIR>`

Where
* APP_NAME is the name of the application you want to record
* INTERVAL_IN_SECS is the interval between frame captures, in seconds
* OUTPUT_DIR is an empty or nonexistant directory to store the frames

You can stop the recording manually with a good 'ol keyboard interrupt, but it'll stop automatically when the window it's recording is closed

TODO
----

* General code cleaning and such, handle errors better
* Better argument parsing
* Add a way to select a particular window instead of guessing that the first one is right
* Do the processing to make a video
