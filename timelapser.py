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
    windowIdsOutput = subprocess.check_output("osascript -e 'tell app \"" + programName + "\" to id of windows'", shell=True)
    windowIds = windowIdsOutput.split(", ")
    windowNamesOutput = subprocess.check_output("osascript -e 'tell app \"" + programName + "\" to name of windows'", shell=True)
    windowNames = windowNamesOutput.split(", ")
except subprocess.CalledProcessError as e:
    print "Something went wrong identifying the windows available to record: " + str(e)
    sys.exit(1)

validWindowIdsAndNames = []
for i, windowId in enumerate(windowIds):
    windowName = windowNames[i]
    if windowId != -1:
        validWindowIdsAndNames.append((windowId, windowName))

if len(validWindowIdsAndNames) <= 0:
    print "Couldn't find any valid windows for " + programName
    sys.exit(1)

if len(validWindowIdsAndNames) == 1:
    windowId = validWindowIdsAndNames[0][0]
else:
    print "Found more than one window, pick from the following list:"
    for i, windowInfo in enumerate(validWindowIdsAndNames):
        print str(i) + ". " + windowInfo[1]

    choiceStr = raw_input("Choice: ")
    try:
        choiceIndex = int(choiceStr)
    except ValueError:
        print "Yo, " + choiceStr + " isn't a number."
        sys.exit(1)

    if choiceIndex < 0 or choiceIndex >= len(validWindowIdsAndNames):
        print "Hey, " + choiceStr + " isn't a valid choice."
        sys.exit(1)

    windowId = validWindowIdsAndNames[choiceIndex][0]

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
            print "Got an exception during recording, cleaning up..."
            break

        currentImage += 1
        time.sleep(captureInterval)
except KeyboardInterrupt:
    print "Cleaning up..."

infoFile.write("Recording ended: " + time.strftime("%Y-%m-%d %H:%M") + "\n\n")
infoFile.write("Captured " + str(currentImage) + " frames at a " + str(captureInterval) + " second interval\n")
infoFile.close()

print "Generating the video..."

videoName = os.path.split(outputDir)[1]
os.chdir(outputDir)

try:
    subprocess.check_call("ffmpeg -i frame-%d.png -c:v libx264 -pix_fmt yuv420p -s 1280x720 " + videoName + ".mp4", shell=True)
except subprocess.CalledProcessError as e:
    print "There was a problem generating the video: " + str(e)

print "Done!"

