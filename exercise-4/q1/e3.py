from contextlib import redirect_stdout
import io
class StandardOutput:
    def __enter__(self):
        self.stdcapture = io.StringIO()
        self.redirect = redirect_stdout(self.stdcapture)
        self.redirect.__enter__()
        return self

    def __exit__(self, exception, error, traceback):
        self.redirect.__exit__(exception, error, traceback)

    @property
    def value(self):
        return self.stdcapture.getvalue()


