#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Contain log related utility functions."""

import logging
import sys


# log_file_format = %(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)
class MyLogger:
    def __init__(self):
        self._logFormatter = logging.Formatter(
            # "%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p"
            "%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)"
        )
        self.program_logger = self._init_program_logger()
        self.debug_logger = self._init_debug_logger()

    def _logging_log_multiple_time(self, logger):
        if len(logger.handlers) >= 1:
            logger.handlers = [logger.handlers[0]]
        return logger

    def _init_program_logger(self):
        self._program_logger_name = 'program logger'
        logger = logging.getLogger(self._program_logger_name)
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)

        handler.setFormatter(self._logFormatter)

        logger.addHandler(handler)

        logger = self._logging_log_multiple_time(logger)

        return logger

    def _init_debug_logger(self):
        self._debug_logger_name = 'debug logger'
        logger = logging.getLogger(self._debug_logger_name)
        logger.setLevel(logging.DEBUG)

        handler = logging.StreamHandler(sys.stdout)

        handler.setFormatter(self._logFormatter)

        # Set Handler Level to DEBUG
        logger.addHandler(handler)

        logger = self._logging_log_multiple_time(logger)

        return logger


if __name__ == '__main__':
    my_logger = MyLogger()
    logger = my_logger.debug_logger
    logger.debug('Debug')
    logger.info('Info')
    logger.critical('Critical')
