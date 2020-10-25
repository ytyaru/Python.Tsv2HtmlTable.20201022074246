import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import ColoredFormatter
import logging

class ColoredLogger(logging.Logger):
#    FORMAT = "[$BOLD%(name)-20s$RESET][%(levelname)-18s]  %(message)s ($BOLD%(filename)s$RESET:%(lineno)d)"
    FORMAT = "[%(levelname)s] %(message)s ($BOLD%(filename)s$RESET:%(lineno)d)"
#    FORMAT = "[%(levelname)s]\t%(message)s\t($BOLD%(filename)s$RESET:%(lineno)d)"
    COLOR_FORMAT = ColoredFormatter.formatter_message(FORMAT, True)
    def __init__(self, name='', level=logging.DEBUG):
        logging.Logger.__init__(self, name, level)
        color_formatter = ColoredFormatter.ColoredFormatter(self.COLOR_FORMAT)
        console = logging.StreamHandler()
        console.setFormatter(color_formatter)
        self.addHandler(console)
        return


logging.setLoggerClass(ColoredLogger)
