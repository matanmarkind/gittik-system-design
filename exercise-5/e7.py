from simple import read_value, write_value

import pathlib
import pytest
import tempfile

@pytest.fixture
def path():
    tmp = tempfile.TemporaryDirectory()
    dpath = pathlib.Path(tmp.name)
    write_value(dpath / 'n.txt', 1)
    write_value(dpath / 's.txt',  'Hello, world!')
    write_value(dpath / 'l.txt', [1, 2, 3, 4, 5])
    yield dpath

def test_read_values(path):
    n = path / 'n.txt'
    assert read_value(n) == 1
    s = path / 's.txt'
    assert read_value(s) == 'Hello, world!'
    l = path / 'l.txt'
    assert read_value(l) == [1, 2, 3, 4, 5]
