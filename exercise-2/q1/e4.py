
import functools, time

def time_execution(f):

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        start = time.time()
        res = f(*args, **kwargs)
        print(f'{f.__name__} took {time.time() - start} seconds to execute')
        return res

    return wrapper