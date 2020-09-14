#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""contains decorator related to time."""


def my_timer(orig_func):
    """Log how long orig_func takes to run."""
    import time
    from functools import wraps

    @wraps(orig_func)
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = orig_func(*args, **kwargs)
        t2 = time.time() - t1
        print(f"{orig_func.__name__} ran in: {t2} sec")
        return result

    return wrapper
