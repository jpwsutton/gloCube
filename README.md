gloCube
=======

Glowing Notification Moodlamp Code

This project consists of a number of python scripts and an Arduino .ino
sketch. Some or all of which might be of use to members of the community that wish
to build similar notification projects.

The related blog post: http://www.jsutton.co.uk/wordpress/?p=190

The wiki page: http://wiki.jsutton.co.uk/doku.php?id=projects:glocube

gloCube.ino
-----------
This Arduino sketch is written for the Teensy++ 2.0 but can be adapted to be
run on a normal Arduino.

It makes use of the SerialCommand Library, which can be found here: https://github.com/scogswell/ArduinoSerialCommand

Once it has been uploaded, useage is as follows:

To use the running code, connect to the serial port and send one of two commands.

```F <LED ID> <R value> <G value> <B value>```

 – This will fade the selected LED to the specified colour e.g. ```F 0 255 0 0``` will fade LED 0 to red.
 
 
```L <Flash No.> <R value> <G value> <B value>```

 – This will flash all LEDs N number of times at the specified colour e.g. ```L 5 0 255 0``` Will flash all LEDs five times green.

To do
-----
- [ ] Convert python/gmail_checker.pl to python (And maybe get rid of the curl command).
- [ ] Separate out some of the logic so that the cube control is done from a module.
- [ ] Make it work on windows.
- [ ] Make it deal with a dropped or missing serial port.


Author
------

James Sutton - Original sketch and python scripts



Thanks
------

* Thanks to Steven Cogswell for the SerialCommand Library used in the Firmware for the Cube -  https://github.com/scogswell/ArduinoSerialCommand
