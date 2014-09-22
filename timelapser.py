import re
import os
import sys
import time
import errno
import subprocess

# Arguments

if len(sys.argv) < 4:
    print "Usage: python timelapser.py <APP_NAME> <INTERVAL_IN_SECS> <OUTPUT_DIR>"
    sys.exit(1)

programName = sys.argv[1]
captureInterval = float(sys.argv[2])
outputDir = sys.argv[3]

try:
    os.makedirs(outputDir)
except OSError as e:
    if e.errno == errno.EEXIST and os.path.isdir(outputDir):
        pass
    else:
        print "Couldn't create the output directory: " + str(e)
        sys.exit(1)

if len(os.listdir(outputDir)) > 0:
    print "The output directory isn't empty! What's up with that?"
    sys.exit(1)

# Getting the window id

try:
    windowsOutput = subprocess.check_output("osascript -e 'tell app \"" + programName + "\" to windows'", shell=True)
    windows = windowsOutput.split(", ")
except subprocess.CalledProcessError as e:
    print "Something went wrong identifying the window to record: " + str(e)
    sys.exit(1)

windowPattern = re.compile("^window id (-?[0-9]+)$")

validWindowIds = []
for window in windows:
    windowMatch = windowPattern.match(window.strip())
    if windowMatch:            
        windowId = int(windowMatch.group(1))
        if windowId != -1:
            validWindowIds.append(windowId)

if len(validWindowIds) <= 0:
    print "Couldn't find any open windows for " + programName
    sys.exit(1)

windowId = validWindowIds[0]

if len(validWindowIds) > 1:
    print "WARNING: Found more than one open window for " + programName + ", guessing the first window (" + str(windowId) + ") is correct!"

# Writing the info file

infoFile = open(os.path.join(outputDir, "recordingInfo.txt"), "w")
infoFile.write("Recording started: " + time.strftime("%Y-%m-%d %H:%M") + "\n")
infoFile.flush()

# Capturing the frames

try:
    currentImage = 0
    while True:
        frameName = os.path.join(outputDir, "frame-" + str(currentImage) + ".png")

        try:
            subprocess.check_call("screencapture -l" + str(windowId) + "-o -x " + frameName, shell=True)
            print "Captured frame " + str(currentImage)
        except subprocess.CalledProcessError as e:
            print "Got an exception during recording, cleaning up and exiting..."
            break

        currentImage += 1
        time.sleep(captureInterval)
except KeyboardInterrupt:
    print "Cleaning up and exiting..."

infoFile.write("Recording ended: " + time.strftime("%Y-%m-%d %H:%M") + "\n\n")
infoFile.write("Captured " + str(currentImage) + " frames\n")
infoFile.close()
