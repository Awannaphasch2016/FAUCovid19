#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Contains functions that returns errors template."""
from typing import Optional
from typing import Tuple

from flask_api import status


def https_400_bad_request_template(error: str) \
        -> Optional[Tuple[str, int]]:

    return (f"HTTPS_400_BAD_REQUEST: {error}", status.HTTP_400_BAD_REQUEST)