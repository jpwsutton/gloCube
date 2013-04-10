#
# Configuration module for glowConnector scripts
# jsutton.co.uk - 2013
#

### Main Configuration ###

serial_port = "/dev/ttyACM0"  # The serial port to use
serial_speed = 9600  # The speed of the port (usually 9600)

default_flashes = 5  # No. of flashes per notification
default_delay = 30  # Delay between cycling the standby colours
update_check_delay = 40  # Seconds to wait before checking for an update

### Update Sources ###

## Facebook ##
facebook_app_id = "APP ID"
facebook_app_secret = "APP SECRET"
facebook_check = 1
facebook_check_colour = "skyblue"
facebook_token_file = ".fb_access_token"

## Gmail ##
gmail_username = "username"
gmail_password = "password"
gmail_check = 1
gmail_check_colour = "red"
