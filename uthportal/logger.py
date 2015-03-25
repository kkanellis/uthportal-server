import logging
import os

class logging_level:
        WARN = logging.WARN
        DEBUG = logging.DEBUG
        ERROR = logging.ERROR
        INFO = logging.INFO


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

    file_formatter = ColoredFormatter(
            "%(asctime)s: [%(levelname)s] [%(name)s] %(message)s",  "%Y-%m-%d %H:%M:%S")

    console_formatter = ColoredFormatter(
            "%(asctime)s: [%(levelname)s] %(message)s",  "%Y-%m-%d %H:%M:%S")

    fh.setFormatter(file_formatter)
    ch.setFormatter(console_formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

#The background is set with 40 plus the number of the color, and the foreground with 30

#These are the sequences need to get colored ouput
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"
COLORS = {
    'WARNING': YELLOW,
    'INFO': WHITE,
    'DEBUG': BLUE,
    'CRITICAL': YELLOW,
    'ERROR': RED
}

class ColoredFormatter(logging.Formatter):
    def __init__(self, fmt, date_fmt, use_color = True):
        super(ColoredFormatter,self).__init__(fmt, date_fmt)
        self.use_color = use_color

    def format(self, record):
        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ
            record.levelname = levelname_color
        return super(ColoredFormatter, self).format(record)
