import functools

def exception_safe(*args):
    errors = ()

    def gen_wrapper(f):

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except errors as e:
                return None
            except Exception as e:
                raise e

        return wrapper

    # If this is decorated without any parens
    if len(args) == 1 and callable(args[0]):
        errors = (Exception)
        return gen_wrapper(args[0])

    # If decorated with parens, contents will be a tupe of errors.
    if len(args) == 0:
        errors = (Exception)
    else:
        errors = args
    return gen_wrapper