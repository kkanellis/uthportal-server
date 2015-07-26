import logging
import logging.handlers
import os
level_dict = {
        'WARN': logging.WARN,
        'DEBUG': logging.DEBUG,
        'ERROR': logging.ERROR,
        'INFO': logging.INFO
}

logging.captureWarnings(True)

def _get_level(name, settings_level):
    if name in settings_level:
        return level_dict[settings_level[name]]
    else:
        return level_dict[settings_level['default']]

def get_logger(name, settings, show_in_terminal = True, override_file_level = False):
    """Creates a custom logger with date and time"""
    folder = settings['log_dir']

    level = _get_level(name, settings['logger']['levels'])

    if not os.path.exists(folder):
        os.makedirs(folder)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG) #Set to the lowest

    #File handler
    fh = logging.handlers.RotatingFileHandler(
            folder + '/' + name + '.log',
            maxBytes=settings['logger']['max_size'],
            backupCount=settings['logger']['logs_backup_count'])
    fh.setLevel(level if override_file_level else logging.DEBUG)
    file_formatter = ColoredFormatter(
            "%(asctime)s: [%(levelname)s] %(message)s",  "%Y-%m-%d %H:%M:%S")

    fh.setFormatter(file_formatter)
    logger.addHandler(fh)

    if show_in_terminal:
        #Congole handler
        ch = logging.StreamHandler()
        ch.setLevel(level)
        console_formatter = ColoredFormatter(
                "%(asctime)s: [%(levelname)s] [%(name)s] %(message)s",  "%Y-%m-%d %H:%M:%S")
        ch.setFormatter(console_formatter)
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
