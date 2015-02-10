import logging
import os

class logging_level():
        WARN = logging.WARN
        DEBUG = logging.debug
        ERROR = logging.ERROR
        INFO = logging.INFO


        #!/usr/bin/env python
def split_filepath(filepath):
    filepath = os.path.abspath(filepath) #ensure we got path
    dirname, filename = os.path.split(filepath)
    filename = os.path.splitext(filename)[0]
    dirname = dirname + "/logs"
    return dirname, filename


def get_logger(filepath, level):
    """Creates a custom logger with date and time"""

    folder, name = split_filepath(filepath)
    if not os.path.exists(folder):
        os.makedirs(folder)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    fh = logging.FileHandler(folder + '/' + name + '.log');
    fh.setLevel(level)

    ch = logging.StreamHandler()
    ch.setLevel(level)

    formatter = logging.Formatter(
            "%(asctime)s: [%(levelname)s]%(message)s",  "%Y-%m-%d %H:%M:%S")

    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger
