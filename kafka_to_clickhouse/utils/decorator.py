from functools import wraps


def get_value_from_generator(func):
    @wraps(func)
    def inner(*args, **kwargs):
        fn_instance = func(*args, **kwargs)
        next(fn_instance)
        return fn_instance

    return inner
