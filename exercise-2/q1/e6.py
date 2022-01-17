import functools

def synchronize(lock):

    def gen_wrapper(f):

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            with lock:
                return f(*args, **kwargs)

        return wrapper

    return gen_wrapper
