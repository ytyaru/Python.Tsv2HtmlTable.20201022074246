import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import ColoredFormatter
import logging

class ColoredLogger(logging.Logger):
#    FORMAT = "[$BOLD%(name)-20s$RESET][%(levelname)-18s]  %(message)s ($BOLD%(filename)s$RESET:%(lineno)d)"
    FORMAT = "[%(levelname)s] %(message)s ($BOLD%(filename)s$RESET:%(lineno)d)"
#    FORMAT = "[%(levelname)s]\t%(message)s\t($BOLD%(filename)s$RESET:%(lineno)d)"
    COLOR_FORMAT = ColoredFormatter.formatter_message(FORMAT, True)
#    def __init__(self, name='', level='DEBUG'):
    def __init__(self, name='', level=logging.DEBUG):
        logging.Logger.__init__(self, name, level)
#        logging.Logger.__init__(self, name, self.__get_level(level))
        color_formatter = ColoredFormatter.ColoredFormatter(self.COLOR_FORMAT)
        console = logging.StreamHandler()
        console.setFormatter(color_formatter)
        self.addHandler(console)
        return
    def __get_level(self, level):
        level = level.lower()
        if   'c' == level: level = 'critical'
        elif 'e' == level: level = 'error'
        elif 'w' == level: level = 'warning'
        elif 'i' == level: level = 'info'
        elif 'd' == level: level = 'debug'
        if level not in ['critical', 'error', 'warning', 'info', 'debug']: level = 'critical'
        return getattr(logging, level.upper())


logging.setLoggerClass(ColoredLogger)
