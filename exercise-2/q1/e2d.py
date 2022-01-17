import functools

# Log traceing example.
def trace(log=print):
    """
    log is a function that takes the log line and flushes it to the correct 
    destination.
    """
    def gen_wrapper(f):
        call_depth = 0
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            nonlocal call_depth
            leading_spaces = ' ' * call_depth
            call_depth += 1

            call = f'{f.__name__}('
            if args:
                call += ', '.join(repr(arg) for arg in args)
            if kwargs:
                call += ', '.join(f'{key}={value!r}' for key, value in kwargs.items())
            call += ')'
            log(f'{leading_spaces}enter {call}')
            try:
                result = f(*args, **kwargs)
                log(f'{leading_spaces}leave {call}: {result!r}')
                return result
            except Exception as error:
                log(f'{leading_spaces}leave {call} on error: {error}')
                raise
            finally:
                call_depth -= 1

        return wrapper
    return gen_wrapper

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
def fib(n):
    return n if n < 2 else fib(n-1) + fib(n-2)

fib(3)
