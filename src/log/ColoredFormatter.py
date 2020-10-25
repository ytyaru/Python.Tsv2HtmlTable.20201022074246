import logging
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

#The background is set with 40 plus the number of the color, and the foreground with 30

#These are the sequences need to get colored ouput
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"

def formatter_message(message, use_color = True):
    if use_color:
        message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message

COLORS = {
    'DEBUG': BLUE,
    'INFO': GREEN,
    'WARNING': YELLOW,
    'ERROR': MAGENTA,
    'CRITICAL': RED,
}

class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color = True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    # https://docs.python.org/ja/3/library/logging.html#logging.LogRecord
    def format(self, record):
        levelname = record.levelname
        if self.use_color and levelname in COLORS:
#            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ
#            record.levelname = levelname_color
#            record.msg = COLOR_SEQ % (30 + COLORS[levelname]) + record.msg + RESET_SEQ
#            for key in ['name', 'levelname', 'pathname', 'lineno', 'msg', 'args', 'exc_info', 'func', 'sinfo']:
#            for key in ['name', 'levelname', 'pathname', 'lineno', 'msg', 'args', 'exc_info']:
            for key in ['name', 'levelname', 'pathname', 'msg']:
                setattr(record, key, COLOR_SEQ % (30 + COLORS[levelname]) + str(getattr(record, key)) + RESET_SEQ)
        return logging.Formatter.format(self, record)
