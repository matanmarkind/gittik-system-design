import contextlib
import tempfile
import io
import time


@contextlib.contextmanager
def timer():
    try:
        timer.started = time.time()
        yield timer
    finally:
        timer.stopped = time.time()
        timer.elapsed = timer.stopped - timer.started


@contextlib.contextmanager
def suppress(*exceptions):
    exceptions = exceptions if exceptions else (Exception)
    try:
        yield
    except exceptions as e:
        pass


@contextlib.contextmanager
def standard_output():
    stdcapture = io.StringIO()
    redirect = contextlib.redirect_stdout(stdcapture)
    with redirect as stdout:
        yield standard_output
    standard_output.value = stdcapture.getvalue()


@contextlib.contextmanager
def temporary_file():
    with tempfile.NamedTemporaryFile() as tf:
        yield tf.name


@contextlib.contextmanager
def temporary_directory():
    with tempfile.TemporaryDirectory() as td:
        yield td