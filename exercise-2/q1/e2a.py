import functools

# Log traceing example.
def trace(f=None, /, *, log=print):
    """
    log is a function that takes the log line and flushes it to the correct 
    destination.
    """
    if f is None:
        return lambda f: trace(f, log=log)

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        log(f'enter {f.__name__}')
        result = f(*args, **kwargs)
        log(f'leave {f.__name__}')
        return result
    return wrapper

# Use a single filehandle for any given log file.
# - `handle` is created outside the scope of `write`, so all calls 
#   to a given logger will reuse the same handle.
# - memoize then means that for any given fname, we will return a
#   a ref to the same logger.
@functools.lru_cache
def logger(fname):
    handle = open(fname, 'a')
    def write(line):
        handle.write(line + '\n')
    return write

@trace
def inc(x):
    return x + 1