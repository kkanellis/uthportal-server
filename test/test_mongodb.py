from __future__ import absolute_import
import logging

from uthportal.database import MongoDatabaseManager
logging.basicConfig(level=logging.DEBUG)


def main():
    manager = MongoDatabaseManager(host='localhost', port=27017)
    result = manager.connect()

    if result:
        manager.disconnect()

    return result

if __name__ == '__main__':
    main()
