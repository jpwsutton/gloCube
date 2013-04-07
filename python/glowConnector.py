#!/usr/bin/python
#
#    Glow Cube Connector V1 - jsutton.co.uk 2013
#

### Libraries ###
import subprocess
import serial
import time
import random
from gi.repository import Notify


### Global Variables ###
# Colour Dictionary
colours = {"red": (204, 0, 0),
           "green": (0, 204, 0),
           "blue": (0, 0, 204),
           "yellow": (204, 204, 0),
           "orange": (204, 102, 0),
           "magenta": (204, 0, 102),
           "mauve": (204, 0, 204),
           "dpink": (255, 10, 133),
           "pink": (225, 71, 163),
           "lgreen": (102, 204, 0),
           "dturquoise": (10, 255, 133),
           "turquoise": (71, 255, 163),
           "purple": (102, 0, 204),
           "skyblue": (0, 102, 204),
           "lblue": (0, 204, 204),
           "mgreen": (0, 204, 102)}

default_flashes = 5  # No. of flashes per notification
default_delay = 30  # Delay between cycling the standby colours

# Update checking variables
update_check_delay = 120  # How many seconds to wait before doing an update

# Colours to flash when an update comes in
email_check_colour = "red"
facebook_check_colour = "skyblue"

# Serial Port
port_name = '/dev/ttyACM0'


### Functions ###

# Send Notification
def notify(subject, message):
    Notify.init(subject)
    message = Notify.Notification.new(subject, message, "dialog-information")
    message.show()

# Fade LED to value


def setLED(ledID, R, G, B):
    serialPort.write('F ' + str(ledID) + ' ' + str(
        R) + ' ' + str(G) + ' ' + str(B) + '\n')

# Flash LED


def flashLED(flashes, R, G, B):
    serialPort.write('L ' + str(flashes) + ' ' + str(
        R) + ' ' + str(G) + ' ' + str(B) + '\n')

# Check Gmail


def checkGmail():
    numOfEmails = subprocess.check_output(["./gmail_checker.pl"]).rstrip()
    # Thank you Sam for this!
    if(int(numOfEmails) > 0):
        print("You have " + str(numOfEmails) + " emails in your inbox!")
        notify("Emails", "You have " + str(
            numOfEmails) + " emails in your inbox!")
        flashLED(default_flashes, colours[email_check_colour][0], colours[
                 email_check_colour][1], colours[email_check_colour][2])

# Check Facebook


def checkFacebook():
    unseen_notifications = subprocess.check_output(
        ["./facebook_checker.py"]).rstrip()
    if(int(unseen_notifications) > 0):
        print("You have " + str(
            unseen_notifications) + " unseen Facebook notifications!")
        notify("Facebook", "You have " + str(
            unseen_notifications) + " unseen Facebook notifications!")
        flashLED(default_flashes, colours[facebook_check_colour][0], colours[
                 facebook_check_colour][1], colours[facebook_check_colour][2])

# Check for updates


def checkUpdates():
    # Get elapsed time
    global start_time
    elapsed_time = time.time() - start_time
    # Has the update_check_delay elapsed?
    if(elapsed_time >= update_check_delay):
        # First, check the email counter
        checkGmail()
        checkFacebook()
        # Reset the clock
        start_time = time.time()


### Main Program ###

# Wait a few seconds, as we are most likely starting as soon as the device is
# plugged in.
notify("Glow Cube Controller", "Starting..")
time.sleep(1)
while 1:
    # Set up serial goodness
    try:
        serialPort = serial.Serial(port_name, 9600)
        print("Serial port created!")
        start_time = time.time()
        while 1:
            checkUpdates()
            for x in range(0, 3):
                myColour = random.choice(colours.keys())
                setLED(x, colours[myColour][0], colours[
                       myColour][1], colours[myColour][2])
            time.sleep(default_delay)
    finally:
        print("Could not open " + port_name +
              ". Will re-attempt connection in 10s")
        time.sleep(10)
