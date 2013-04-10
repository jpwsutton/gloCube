#!/usr/bin/python
#
#    Glow Cube Connector V1 - jsutton.co.uk 2013
#

### Libraries ###
import subprocess
import serial
import time
import random
import feedparser
import facebook
import os.path
import pickle

from gi.repository import Notify

### Import Settings ###
from glowConfig import *
print("> Imported Settings.")

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
    gmail_feed = feedparser.parse(
        'https://' + gmail_username + ':' + gmail_password +
        '@mail.google.com/mail/feed/atom')
    # Thank you Sam for this!
    if(int(gmail_feed.feed.fullcount) > 0):
        print("You have " + str(numOfEmails) + " emails in your inbox!")
        notify("Emails", "You have " + str(
            numOfEmails) + " emails in your inbox!")
        flashLED(default_flashes, colours[gmail_check_colour][0], colours[
                 gmail_check_colour][1], colours[gmail_check_colour][2])


# Check Facebook
def checkFacebook():
    try:
        graph = facebook.GraphAPI(fb_token)
        notifications = graph.get_connections("me", "notifications")
        if len(notifications['summary']) != 0:
            unseen_notifications = notifications['summary']['unseen_count']
            if(int(unseen_notifications) > 0):
                print("> You have " + str(
                      unseen_notifications) +
                      " unseen Facebook notifications!")
                notify("Facebook", "You have " + str(
                       unseen_notifications) +
                       " unseen Facebook notifications!")
                flashLED(default_flashes, colours[facebook_check_colour][0],
                         colours[facebook_check_colour][1],
                         colours[facebook_check_colour][2])
    except:
        print("> There was an error checking facebook status.")

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

# Wait a second, as we are most likely starting as soon as the device is
# plugged in.
print("> Starting Glow Cube Controller..")
notify("Glow Cube Controller", "Starting..")

# First we do a check to see if we have the token for facebook
if not os.path.exists(facebook_token_file):
    print("> No token found, Logging into facebook for the first time...")
    notify("Glow Cube Controller",
           "No token found, Logging into facebook for the first time.")
    subprocess.check_output(["/home/james/scripts/facebook_login.py"])
fb_token = pickle.load(open(facebook_token_file, "rb"))

time.sleep(1)
conn_count = 0

while(conn_count < 5):
    # Set up serial goodness
    try:
        print("> Connecting...")
        serialPort = serial.Serial(serial_port, serial_speed)
        print("> Serial port " + serial_port + " opened.")
        start_time = time.time()
        while 1:
            checkUpdates()
            for x in range(0, 3):
                myColour = random.choice(colours.keys())
                setLED(x, colours[myColour][0], colours[
                       myColour][1], colours[myColour][2])
            time.sleep(default_delay)
    except serial.SerialException as e:
        print("> Serial Error: " + str(e))
    time.sleep(2)
    conn_count = conn_count + 1
print("> Glow Cube Controller Stopping.")
