#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Contain log related utility functions."""

import logging

# create logger
module_logger = logging.getLogger("logger_module.auxiliary")

LOGGER_NAME = 'logger_class'


class Auxiliary:
    def __init__(self):
        self.logger = logging.getLogger(f"{LOGGER_NAME}")
        self.logger.info("Creating an instance of Auxiliary...")
        self._prepare_logger()

    # def do_something(self):
    #     self.logger.info("doing something")
    #     a = 1 + 1
    #     self.logger.info("done doing something")
    #     self.logger.error("error")
    #     self.logger.debug("debug")

    def _prepare_logger(self):
        self._init_program_logger()
        self._init_error_logger()

    def _init_program_logger(self):
        self.program_logger = logging.StreamHandler()

        logger = logging.getLogger("spam_application")
        self.program_logger.setLevel(logging.ERROR)

        # create formatter and add it to the handlers
        formatter1 = logging.Formatter("%(message)s")
        self.program_logger.setFormatter(formatter1)

        # add the handlers to the logger
        logger.addHandler(self.program_logger)

    def _init_error_logger(self):
        self.program_logger = logging.StreamHandler()

        logger = logging.getLogger("spam_application")
        self.program_logger.setLevel(logging.ERROR)

        # create formatter and add it to the handlers
        formatter1 = logging.Formatter("%(message)s")
        self.program_logger.setFormatter(formatter1)

        # add the handlers to the logger
        logger.addHandler(self.program_logger)


def some_function():
    module_logger.info(f"received a call to {some_function.__name__}")
