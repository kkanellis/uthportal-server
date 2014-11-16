from __future__ import absolute_import
import logging

from uthportal.database import MongoDatabaseManager
logging.basicConfig(level=logging.DEBUG)


def main():
    manager = MongoDatabaseManager(host='localhost', port=27017)
    if manager.connect():
        print("\t Module test successful")
    else :
        print("Module failed!")

    manager.disconnect()

if __name__ == '__main__':
    main()
