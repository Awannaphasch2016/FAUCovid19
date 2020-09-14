#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""contains decorators related to logging."""

import logging


def log_error(func):
    """Log if error occurs."""

    def no_error(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(str(e))
            return None

    return no_error


def signature_logger(orig_func):
    """Log passed in argument and name of orig_func."""
    import logging

    logging.basicConfig(
        filename=f"{orig_func.__name__}.log",
        level=logging.INFO,
    )
    from functools import wraps

    @wraps(orig_func)
    def wrapper(*args, **kwargs):
        logging.info(f"Ran with args: {args}, and kwargs: {kwargs}")
        return orig_func(*args, **kwargs)

    return wrapper
