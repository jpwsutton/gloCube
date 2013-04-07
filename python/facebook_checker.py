#!/usr/bin/python
#
#    Facebook notification checker V1 - jsutton.co.uk 2013
#

### Libraries ###
import facebook
import os.path
import subprocess
import pickle


### Variables ###
LOCAL_FILE = '.fb_access_token'

# First we do a check to see if we have the token / user data
if not os.path.exists(LOCAL_FILE):
    print("No token found, Logging into facebook for the first time...")
    subprocess.check_output(["./facebook_login.py"])


fb_token = pickle.load(open(LOCAL_FILE, "rb"))
# print("Facebook Token: " + fb_token)


# Setting up Graph API
try:
    graph = facebook.GraphAPI(fb_token)
    notifications = graph.get_connections("me", "notifications")
    if len(notifications['summary']) != 0:
        unseen_count = notifications['summary']['unseen_count']
        # print("You have " + str(unseen_count) + " unseen notifications")
        print str(unseen_count)
    else:
        print "0"
except:
    print "0"
