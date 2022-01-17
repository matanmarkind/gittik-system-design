import functools, inspect

def validate_types(**types):

    def gen_wrapper(f):

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            for name, val in inspect.getcallargs(f, *args, **kwargs).items():
                if type(val) != types[name]:
                    raise ValueError

            res = f(*args, **kwargs)
            assert type(res) == types['return_value']
            return res

        return wrapper

    return gen_wrapper
