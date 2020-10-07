#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Contains functions that returns errors template."""
from typing import Optional
from typing import Tuple

from flask_api import status  # type: ignore

from src.Utilities.Logging import MyLogger

LOGGER = MyLogger()
PROGRAM_LOGGER = LOGGER.program_logger


def https_400_bad_request_template(error: str) \
        -> Tuple[str, int]:

    return (f"HTTPS_400_BAD_REQUEST: {error}", status.HTTP_400_BAD_REQUEST)