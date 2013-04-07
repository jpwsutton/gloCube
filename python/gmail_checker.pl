#!/usr/bin/perl -w
###########################################################################
#                                                                         # 
#                      Gmail Notification checker                         # 
#                           jsutton - 2012                                # 
#                        Returns number of unread emails.                 # 
#                                                                         # 
###########################################################################

######################### Imports #########################
use strict;
use warnings;


######################## Variables ########################
my $username = 'USERNAME';
my $password = 'PASSWORD';

my $command = "curl -u $username:$password --silent \"https://mail.google.com/mail/feed/atom\" | tr -d '\\n' | awk -F '<entry>' '{for (i=2; i<=NF; i++) {print \$i}}' | sed -n \"s/<title>\\(.*\\)<\\/title.*name>\\(.*\\)<\\/name>.*/\\2 - \\1/p\" | wc -l";

	
########################### Main ##########################
my $response = `$command`;
print "$response";

