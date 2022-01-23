class Suppress:
    def __init__(self, *exceptions_to_suppress):
        self.exceptions_to_suppress = exceptions_to_suppress

    def __enter__(self):
        pass

    def __exit__(self, exception, error, traceback):
        suppress_all = not self.exceptions_to_suppress
        return exception in self.exceptions_to_suppress or suppress_all
