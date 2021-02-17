#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Contains untilites functions that don't belong to other categories."""
from typing import Optional
from typing import Union

from flask_api import status  # type: ignore

from src.Utilities.DeclaredTyping.other_typing import ErrorWithMssage


def return_error_template(has_error: ErrorWithMssage
                          ) -> Optional[Union[ErrorWithMssage, str]]:
    try:
        if status.HTTP_400_BAD_REQUEST == has_error[1]:
            return has_error
    except:
        return "ERROR is not properly caught, unknown error is returned."
    return None
