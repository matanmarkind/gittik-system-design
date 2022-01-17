import functools

def cache(f):
    generation = 0
    cache = {}

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        key = args + tuple((k, v) for k, v in kwargs.items())
        if key not in cache:
            cache[key] = f(*args, **kwargs)
        return cache[key]

    wrapper.cache = cache
    return wrapper

