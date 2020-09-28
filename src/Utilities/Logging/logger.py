#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Contain log related utility functions."""

import logging

# create logger
module_logger = logging.getLogger("logger_module")


class MyLogger:
    LOGGER_NAME = 'logger_class'

    def __init__(self):
        self._prepare_loggers()

    def _prepare_loggers(self):
        self.logger = logging.getLogger("spam_application")
        self._init_program_logger()
        self._init_error_logger()

    def _init_program_logger(self):
        self.program_logger = logging.StreamHandler()

        self.program_logger.setLevel(logging.INFO)
        self.program_logger.setLevel(logging.WARNING)

        # create formatter and add it to the handlers
        formatter1 = logging.Formatter("%(message)s")
        self.program_logger.setFormatter(formatter1)

        # add the handlers to the logger
        self.logger.addHandler(self.program_logger)

    def _init_error_logger(self):
        self.error_logger = logging.StreamHandler()

        self.program_logger.setLevel(logging.ERROR)
        formatter1 = logging.Formatter("%(message)s")
        self.program_logger.setFormatter(formatter1)

        self.logger.addHandler(self.program_logger)

    def _init_debug_logger(self):
        self.debug_logger = logging.StreamHandler()

        self.program_logger.setLevel(logging.DEBUG)
        formatter1 = logging.Formatter("%(message)s")
        self.program_logger.setFormatter(formatter1)

        self.logger.addHandler(self.program_logger)



def some_function():
    module_logger.info(f"received a call to {some_function.__name__}")


if __name__ == '__main__':
    pass
