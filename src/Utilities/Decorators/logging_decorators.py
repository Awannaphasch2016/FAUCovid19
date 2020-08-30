import logging


def log_error(func):
    def no_error(*args, **kwargs):
        try:
            return func(*args, ** kwargs)
        except Exception as e:
            logging.error(str(e))
            return None
    return no_error

def signature_logger(orig_func):
    import logging
    logging.basicConfig(filename='{}.log'.format(orig_func.__name__),
                        level=logging.INFO)
    from functools import wraps

    @wraps(orig_func)
    def wrapper(*args, **kwargs):
        logging.info(
           'Ran with args: {}, and kwargs: {}'.format(args, kwargs))
        return orig_func(*args, **kwargs)

    return wrapper
