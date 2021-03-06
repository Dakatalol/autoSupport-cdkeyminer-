from functools import wraps
import logging


def log_exception(message, logger=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if logger is None:
                _self = args[0]  # self
                log = getattr(_self, 'logger')
            else:
                log = logger
            assert isinstance(log, logging.Logger)
            try:
                return func(*args, **kwargs)
            except Exception:
                log.error(message.format(args[1]))
                raise

        return wrapper

    return decorator
