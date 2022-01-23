import time

class Timer:
    def __enter__(self):
        self.started = time.time()
        return self

    def __exit__(self, exception, error, traceback):
        self.stopped = time.time()

    @property
    def elapsed(self):
        return self.stopped - self.started