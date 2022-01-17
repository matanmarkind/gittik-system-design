import functools

def cache(f=None, /, *, max_size=0):
    if f is None:
        return lambda f: cache(f, max_size=max_size)

    generation = 0
    cached_results = {}

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        nonlocal generation
        generation += 1
        key = args + tuple((k, v) for k, v in kwargs.items())

        if key not in cached_results:
            # Unknown value, calculate it.
            cached_results[key] = (f(*args, **kwargs), generation)

            if max_size > 0 and len(cached_results) > max_size:
                # The cache is too large.
                lru_key, lru_gen = key, generation
                for k, (_ ,gen) in cached_results.items():
                    if gen < lru_gen:
                        lru_key, lru_gen = k, gen
                del cached_results[lru_key]

        res, _ = cached_results[key]
        cached_results[key] = res, generation
        return res

    wrapper.cache = cached_results
    return wrapper

