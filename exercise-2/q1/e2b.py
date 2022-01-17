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
        call = f'{f.__name__}('
        if args:
            call += ', '.join(repr(arg) for arg in args)
        if kwargs:
            call += ', '.join(f'{key}={value!r}' for key, value in kwargs.items())
        call += ')'
        log(f'enter {call}')
        try:
            result = f(*args, **kwargs)
            log(f'leave {call}: {result!r}')
            return result
        except Exception as error:
            log(f'leave {call} on error: {error}')
            raise
    return wrapper

# Use a single filehandle for any given log file.
# - `handle` is created outside the scope of `write`, so all calls 
#   to a given logger will reuse the same handle.
# - cache then means that for any given fname, we will return a
#   a ref to the same logger.
@functools.lru_cache
def logger(fname):
    handle = open(fname, 'a')
    def write(line):
        handle.write(line + '\n')
    return write


@trace(log=logger('/tmp/log.txt'))
def inc_log(x):
    return x + 1

@trace
def inc(x):
    return x + 1