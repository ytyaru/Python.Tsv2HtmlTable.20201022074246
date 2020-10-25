#!/usr/bin/env python3
# coding: utf8
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import logging, ColoredLogger
logger = ColoredLogger.ColoredLogger()
#logger = ColoredLogger.ColoredLogger(name='AAA', level=logging.ERROR)
logger.critical('クリティカル')
logger.error('エラー')
logger.warning('ワーニング')
logger.info('インフォ')
logger.debug('デバッグ')
