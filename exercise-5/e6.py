from decimal import DivisionByZero
from simple import mul, div, greet, write_value, read_value

import pytest

@pytest.mark.parametrize(
    'x, y',
    [
        (1, 2),
        (1, 3),
        (2, 2),
        (2, 3),
    ]
)
def test_mul(x, y):
    assert mul(x, y) == x * y


@pytest.mark.parametrize(
    'x, y',
    [
        (1, 0),
        (-1, 0),
    ]
)
def test_mul_zero(x, y):
    assert mul(x, y) == x * y


@pytest.mark.parametrize(
    'x, y',
    [
        (1, 2),
        (-1, 3),
    ]
)
def test_mul_negative(x, y):
    assert mul(x, y) == x * y


@pytest.mark.parametrize(
    'x, y',
    [
        (1/4, 7),
        (-1/4, 8),
        (1/4, 7/3),
    ]
)
def test_mul_fraction(x, y):
    assert mul(x, y) == x * y


def test_div():
    assert div(1, 2) == 1 / 2


def test_div_negative():
    assert div(-1, 2) == -1 / 2


def test_div_fraction():
    assert div(1/2, 2) == (1/2) / 2


def test_div_error():
    with pytest.raises(ZeroDivisionError):
        div(1/0)


def test_greet(capsys):
    greet('Matan')
    captured = capsys.readouterr()
    assert captured.out == 'Hello, Matan!\n'


def test_greet_stranger(capsys):
    greet()
    captured = capsys.readouterr()
    assert captured.out == 'Hello, stranger!\n'


def check_write_read_value(fpath, val):
    write_value(fpath, val)
    assert read_value(fpath) == val

def test_read_value_int(tmp_path):
    for v in [1, 2]:
        check_write_read_value(tmp_path / 'file.txt', v)


def test_read_value_str(tmp_path):
    for v in ['foo', 'bar']:
        check_write_read_value(tmp_path / 'file.txt', v)


def test_read_value_list(tmp_path):
    for v in [[1, 2, 3], []]:
        check_write_read_value(tmp_path / 'file.txt', v)