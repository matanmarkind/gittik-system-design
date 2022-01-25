import os
import contextlib
import sys

@contextlib.contextmanager
def in_directory(path):
    pwd = sys.path.pop()
    orig = sys.path[0] 
    try:
        sys.path[0] = path
        os.chdir(path)
        yield
    except Exception as e:
        print(e)
        raise e
    finally:
        sys.path[0] = orig
        os.chdir(pwd)
