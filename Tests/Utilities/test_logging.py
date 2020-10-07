#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Contain test for logging function."""

import logging

import pytest

from src.Utilities.Logging.logger import MyLogger



@pytest.mark.test_utility_function
def test_program_logger(caplog):
    with caplog.at_level(logging.DEBUG):
        my_logger = MyLogger()
        logger = my_logger.debug_logger
        logger.debug('Debug')
        logger.info('Info')
        logger.critical('Critical')

        assert caplog.record_tuples[0][0] == my_logger._debug_logger_name
        assert caplog.record_tuples[0][1] == logging.DEBUG
