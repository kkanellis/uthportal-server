#!/usr/bin/env python2.7

import signal
import sys
from time import sleep

from uthportal import UthPortal
from uthportal.logger import get_logger

uth_portal = None

def signal_handler(signal, frame):
    uth_portal.logger.info('User interrupt! Exiting....')

    uth_portal.stop()
    sys.exit(0)

def main():
    #Handle SIGINT
    signal.signal(signal.SIGINT, signal_handler)

    global uth_portal
    uth_portal = UthPortal()
    uth_portal.start()

    uth_portal.logger.info('Uthportal started successfully!')
    uth_portal._force_update()

    get_logger('py.warnings', uth_portal.settings)

    while True:
        sleep(2)

if __name__ == '__main__' :
    main()
