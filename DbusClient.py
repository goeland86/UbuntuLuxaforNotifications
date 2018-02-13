#!/usr/bin/env python3
from _dbus_glib_bindings import DBusGMainLoop

from gi.repository import GLib
import dbus

from pyluxafor import LuxaforFlag
from time import sleep

green = [[LuxaforFlag.LED_ALL, 0, 255, 0]]
red = [[LuxaforFlag.LED_ALL, 255, 0, 0]]
yellow = [[LuxaforFlag.LED_ALL, 255, 192, 0]]
confused = [[LuxaforFlag.LED_BACK_SIDE, 255, 0, 0],[LuxaforFlag.LED_TAB_SIDE, 0, 255, 0]]
extra_confused = [
    [LuxaforFlag.LED_TAB_1, 255, 0, 0],
    [LuxaforFlag.LED_TAB_2, 0, 64, 64],
    [LuxaforFlag.LED_TAB_3, 0, 255, 0],
    [LuxaforFlag.LED_BACK_1, 0, 255, 255],
    [LuxaforFlag.LED_BACK_2, 0, 0, 255],
    [LuxaforFlag.LED_BACK_3, 255, 0, 255]
]
blue = [[LuxaforFlag.LED_BACK_1, 0, 0, 255]]

state = green

flag = LuxaforFlag()


def setColor(flagstatus):
    global state, flag
    state = flagstatus
    for ledSet in flagstatus :
        flag.do_static_colour(leds=ledSet[0], r=ledSet[1], g=ledSet[2], b=ledSet[3])


def notifications(bus, message):
    # print(message)
    keys = ["app_name", "replaces_id", "app_icon", "summary","body", "actions", "hints", "expire_timeout"]
    args = message.get_args_list()
    if len(args) == 8:
        notification = dict([(keys[i], args[i]) for i in range(8)])
        if notification["body"] == 'BUSY':
            setColor(red)
        elif notification["body"] == 'QUIET':
            setColor(yellow)
        elif notification["body"] == 'OPEN':
            setColor(green)
        elif notification["body"] == 'COPS':
            flag.do_pattern(LuxaforFlag.PATTERN_POLICE, 3)
            sleep(3)
            setColor(state)
        elif notification["body"] == 'CONFUSED':
            setColor(confused)
        elif notification["body"] == 'EXTRA_CONFUSED':
            setColor(extra_confused)
        elif notification["app_name"] == "Thunderbird":
            if "Successful" in notification["summary"] :
                flag.do_strobe(green[0][0], green[0][1], green[0][2], green[0][3], 5, 5)
            elif "Build Failed" in notification["summary"]:
                flag.do_strobe(red[0][0], red[0][1], red[0][2], red[0][3], 5, 5)
            elif "Build Unstable" in notification["summary"]:
                flag.do_strobe(blue[0][0], yellow[0][1], yellow[0][2], yellow[0][3], 5, 5)
            else:
                flag.do_strobe(blue[0][0], blue[0][1], blue[0][2], blue[0][3], 5, 5)
            sleep(5)
            setColor(state)
        elif notification["body"] == 'LUNCH':
            flag.do_pattern(LuxaforFlag.PATTERN_RAINBOWWAVE, 200)
        elif notification["app_name"] != 'Deezer' and notification["app_name"] != 'gnome-settings-daemon':
            flag.do_strobe(state[0][0], state[0][1], state[0][2], state[0][3], 3, 5)


DBusGMainLoop(set_as_default=True)

session_bus = dbus.SessionBus()
session_bus.add_match_string("type='method_call',interface='org.freedesktop.Notifications',member='Notify',eavesdrop=true")
session_bus.add_message_filter(notifications)

mainloop = GLib.MainLoop()
mainloop.run()
