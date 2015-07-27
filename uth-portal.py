#!/usr/bin/env python2.7

import signal
import sys
import threading
from time import sleep

from uthportal import UthPortal
from uthportal.logger import get_logger

uth_portal = None
socket_server = None

def signal_handler(signal, frame):
    if uth_portal:
        uth_portal.logger.info('User interrupt! Exiting....')

        uth_portal.stop()
    if socket_server:
        socket_server.shutdown()

    sys.exit(0)

def main():
    #Handle SIGINT
    signal.signal(signal.SIGINT, signal_handler)

    global uth_portal, socket_server
    uth_portal = UthPortal()
    uth_portal.start()

    uth_portal.logger.info('Uthportal started successfully!')
    #uth_portal._force_update()

    get_logger('py.warnings', uth_portal.settings)

    while True:
        sleep(2)


if __name__ == '__main__' :
    main()
