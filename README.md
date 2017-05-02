# UbuntuLuxaforNotifications
A simple script to catch DBus notifications and show them on the Luxafor.

It is written in Python3 and depends on [PyLuxafor](https://pyluxafor.readthedocs.io/en/latest/index.html)

Features:

Stores the state of the flag (color), and flashes it in that color when a notification is received that is not from Deezer (my music player, change it at will)

Reading notifications' body for keywords to set the flag's color and state:

    OPEN -> green
    QUIET -> yellow
    BUSY -> red
    CONFUSED -> green tab, red back
    EXTRA_CONFUSED -> each LED a separate color
    COPS -> launch the US police pattern for 3 seconds before going back to the original state
    
  These notification tests can be generated with the command 'notify-send " " \<keyword\>
  
  If the notification is sent by Thunderbird, it flashes slowly in blue for 5 seconds then returns to the original state
  
