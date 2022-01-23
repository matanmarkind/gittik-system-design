import time

class ContextManager:
    def __init__(self, g):
        self.g = g()

    def __enter__(self):
        return next(self.g)

    def __exit__(self, exception, error, traceback):
        if exception is not None:
            self.g.throw(exception)
            return
        try:
            next(self.g)
        except StopIteration as e:
            pass
            