import tempfile, os

class TemporaryFile():
    def __enter__(self):
        self.tempfile = tempfile.NamedTemporaryFile()
        self.tempfile.__enter__()
        return self.tempfile.name

    def __exit__(self, exception, error, traceback):
        self.tempfile.__exit__(exception, error, traceback)


if __name__ == '__main__':
    with TemporaryFile() as f:
        print('Hello, world', f)
        assert os.path.isfile(f)
    assert not os.path.exists(f)