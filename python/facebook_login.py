#!/usr/bin/python
#
# Thanks to pcardune for this script -  http://blog.carduner.net/2010/05/26/authenticating-with-facebook-on-the-command-line-using-python/
# This version has been modified to work with glowCube
#


import os.path
import json
import urllib2
import urllib
import urlparse
import BaseHTTPServer
import webbrowser
import pickle


### Import Settings ###
from glowConfig import *
print("> Imported Settings.")

APP_ID = facebook_app_id
APP_SECRET = facebook_app_secret
ENDPOINT = 'graph.facebook.com'
REDIRECT_URI = 'http://127.0.0.1:8080/'
ACCESS_TOKEN = None
LOCAL_FILE = '.fb_access_token'
STATUS_TEMPLATE = u"{name}\033[0m: {message}"


def get_url(path, args=None):
    args = args or {}
    if ACCESS_TOKEN:
        args['access_token'] = ACCESS_TOKEN
    if 'access_token' in args or 'client_secret' in args:
        endpoint = "https://"+ENDPOINT
    else:
        endpoint = "http://"+ENDPOINT
    return endpoint+path+'?'+urllib.urlencode(args)


def get(path, args=None):
    return urllib2.urlopen(get_url(path, args=args)).read()


class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self):
        global ACCESS_TOKEN
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        code = urlparse.parse_qs(urlparse.urlparse(
            self.path).query).get('code')
        code = code[0] if code else None
        if code is None:
            self.wfile.write("Sorry, authentication failed.")
            sys.exit(1)
        response = get('/oauth/access_token', {'client_id': APP_ID,
                                               'redirect_uri': REDIRECT_URI,
                                               'client_secret': APP_SECRET,
                                               'code': code})
        ACCESS_TOKEN = urlparse.parse_qs(response)['access_token'][0]
        pickle.dump(ACCESS_TOKEN, open(LOCAL_FILE, "wb"))
        self.wfile.write("You have successfully logged in to facebook. "
                         "You can close this window now.")


if __name__ == '__main__':
    if not os.path.exists(LOCAL_FILE):
        print "Logging you in to facebook..."
        webbrowser.open(get_url('/oauth/authorize',
                                {'client_id': APP_ID,
                                 'redirect_uri': REDIRECT_URI,
                                 'scope': 'read_stream,manage_notifications'}))

        httpd = BaseHTTPServer.HTTPServer(('127.0.0.1', 8080), RequestHandler)
        while ACCESS_TOKEN is None:
            httpd.handle_request()
