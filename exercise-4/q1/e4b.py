import tempfile, os

class TemporaryDirectory():
    def __enter__(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.tempdir.__enter__()
        return self.tempdir.name

    def __exit__(self, exception, error, traceback):
        self.tempdir.__exit__(exception, error, traceback)


if __name__ == '__main__':
    with TemporaryDirectory() as d:
        print(d)
        assert os.path.isdir(d)
    assert not os.path.exists(d)