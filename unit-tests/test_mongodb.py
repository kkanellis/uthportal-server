from __future__ import absolute_import

from uthportal.database.mongo import MongoDatabaseManager


def main():
    manager = MongoDatabaseManager(host='localhost', port=27017, db_name='test_db')
    result = manager.connect()
    manager.disconnect()

    if result:
        manager.disconnect()

    return result

if __name__ == '__main__':
    main()
