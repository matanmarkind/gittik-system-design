import functools

def cache(max_size = 0):

    def gen_wrapper(f):
        generation = 0
        cache = {}

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            nonlocal generation
            generation += 1
            key = args + tuple((k, v) for k, v in kwargs.items())

            if key not in cache:
                # Unknown value, calculate it.
                cache[key] = (f(*args, **kwargs), generation)

                if max_size > 0 and len(cache) > max_size:
                    # The cache is too large.
                    lru_key, lru_gen = key, generation
                    for k, (_ ,gen) in cache.items():
                        if gen < lru_gen:
                            lru_key, lru_gen = k, gen
                    del cache[lru_key]

            res, _ = cache[key]
            cache[key] = res, generation
            return res

        wrapper.cache = cache
        return wrapper
    return gen_wrapper

