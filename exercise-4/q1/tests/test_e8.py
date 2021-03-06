import pytest

from e8 import Overloaded


def test_overload():
    class A(metaclass=Overloaded):
        def f(self):
            return 1
        def f(self, x):
            return x
        def f(self, x, y):
            return x + y
    a = A()
    assert a.f() == 1
    assert a.f(1) == 1
    assert a.f(2) == 2
    assert a.f(1, 2) == 3
    assert a.f(2, 2) == 4
