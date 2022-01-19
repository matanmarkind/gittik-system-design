class LazyExpression:
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return self.expr
    
    def evaluate(self, **values):
        return eval(self.expr, values)

class LazyVariable(LazyExpression):
    def build(lhs, op, rhs):
        return LazyVariable(f'({lhs} {op} {rhs})')

    def __add__(self, other):
        return LazyVariable(f'({self.expr} + {other})')

    def __radd__(self, other):
        return LazyVariable(f'({other} + {self.expr})')

    def __sub__(self, other):
        return LazyVariable(f'({self.expr} - {other})')

    def __rsub__(self, other):
        return LazyVariable(f'({other} - {self.expr})')

    def __mul__(self, other):
        return LazyVariable(f'({self.expr} * {other})')

    def __rmul__(self, other):
        return LazyVariable(f'({other} * {self.expr})')

    def __truediv__(self, other):
        return LazyVariable(f'({self.expr} / {other})')

    def __rtruediv__(self, other):
        return LazyVariable(f'({other} / {self.expr})')

    def __floordiv__(self, other):
        return LazyVariable(f'({self.expr} // {other})')

    def __rfloordiv__(self, other):
        return LazyVariable(f'({other} // {self.expr})')

    def __neg__(self):
        return LazyVariable(f'-{self.expr}')

    def __pos__(self):
        return LazyVariable(f'+{self.expr}')

x = LazyVariable('x')
print(x)
print(x + 1)
print(2*x + 1)
print(x.evaluate(x=2))
y = 2*x + 1
print(y.evaluate(x=2))