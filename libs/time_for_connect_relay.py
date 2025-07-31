from random import randint

from libs.connecting import Configuration


def time_for_sleep_after_disconnect():
    if Configuration.sleep_after_disconnect == 0:
        sleep_time_after_disconnect = randint(13, 20)
    elif isinstance(Configuration.sleep_after_disconnect, list):
        sleep_time_after_disconnect = randint(int(Configuration.sleep_after_disconnect[0]),
                                              int(Configuration.sleep_after_disconnect[1]))
    else:
        sleep_time_after_disconnect = Configuration.sleep_after_disconnect
    return sleep_time_after_disconnect


def time_for_sleep_after_reconnect():
    if Configuration.sleep_after_reconnect == 0:
        sleep_time_after_reconnect = randint(13, 20)
    elif isinstance(Configuration.sleep_after_reconnect, list):
        sleep_time_after_reconnect = randint(int(Configuration.sleep_after_reconnect[0]),
                                             int(Configuration.sleep_after_reconnect[1]))
    else:
        sleep_time_after_reconnect = Configuration.sleep_after_reconnect
    return sleep_time_after_reconnect
