#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Contain log related utility functions."""

import logging

# create logger
from typing import List


class MyLogger:
    LOGGER_NAME = 'logger_class'

    def __init__(self):
        self._prepare_loggers()

    def _prepare_loggers(self):
        self.logger = logging.getLogger("spam_application")
        self._init_program_logger()
        self._init_error_logger()

    def _get_formatter(self) -> logging.Formatter:
        formatter = logging.Formatter(
            "%(levelname)s  - %(asctime)s: %(message)s"
        )
        return formatter

    def _set_logger(self,
                    log_handler: logging.Handler,
                    log_level: List[int],
                    ) -> None:
        for i in log_level:
            log_handler.setLevel(i)

        log_handler.setFormatter(self._get_formatter())
        self.logger.addHandler(log_handler)

    def _init_program_logger(self):
        self.program_logger = logging.StreamHandler()

        self.program_logger.setLevel(logging.INFO)
        self.program_logger.setLevel(logging.WARNING)

        # create formatter and add it to the handlers
        self.program_logger.setFormatter(self._get_formatter())

        # add the handlers to the logger
        self.logger.addHandler(self.program_logger)

    def _init_error_logger(self):
        self.error_logger = logging.StreamHandler()

        self.program_logger.setLevel(logging.ERROR)
        self.program_logger.setFormatter(self._get_formatter())

        self.logger.addHandler(self.program_logger)

    def _init_debug_logger(self):
        self.debug_logger = logging.StreamHandler()

        self.program_logger.setLevel(logging.DEBUG)
        self.program_logger.setFormatter(self._get_formatter())

        self.logger.addHandler(self.program_logger)


def some_function():
    module_logger.info(f"received a call to {some_function.__name__}")


if __name__ == '__main__':
    pass
