#!/usr/bin/env python2.7

import signal
import sys
import threading
from time import sleep

from uthportal import UthPortal
from uthportal.logger import get_logger
from uthportal.networking import ThreadedSocketServer

uth_portal = None
socket_server = None

def signal_handler(signal, frame):
    if uth_portal:
        uth_portal.logger.info('User interrupt! Exiting....')
        uth_portal.stop()

    if socket_server:
        socket_server.shutdown()

        sys.exit(0)

def auth_function(info):
    #info should be a means of authentication
    #TODO:implement this
    if info[0] == 'uthportal' and info[1] == "HardPass123":
        return True
    else:
        return False

def handle_command(command):
    return "Command handled by uthportal :" + command

def main():
    #Handle SIGINT
    signal.signal(signal.SIGINT, signal_handler)

    global uth_portal, socket_server
    uth_portal = UthPortal()
    uth_portal.start()

    uth_portal.logger.info('Uthportal started successfully!')
    #uth_portal._force_update()

    get_logger('py.warnings', uth_portal.settings)
    socket_server  = ThreadedSocketServer(uth_portal.settings)
    socket_server.set_handle_function(handle_command)
    socket_server.set_auth_function(auth_function)
    socket_server.listen()

    while True:
        sleep(2)


if __name__ == '__main__' :
    main()
