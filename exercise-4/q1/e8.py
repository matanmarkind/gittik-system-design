import re

def is_public_function(name, fn):
    return callable(fn) and not name.startswith('__')

class OverloadFunction:
    error_pattern = re.compile('.*positional argument.*')

    def __init__(self):
        self.functions = []

    def __repr__(self):
        name = self.__class__.__name__
        num_overloads = len(self.functions)
        overloads = self.functions
        return f'{name}({num_overloads=} {overloads=})'
    
    def __get__(self, instance, cls):
        # Required to get the actual method's `self` before `__call__`.
        self.instance = instance
        return self

    def __call__(self, *args, **kwargs):
        for fn in self.functions:
            try:
                return fn(self.instance, *args, **kwargs)
            except TypeError as e:
                if not self.error_pattern.match(str(e)):
                    raise
        
        raise NameError("Function isn't defined")

    def append(self, f):
        self.functions.append(f)

class OverloadDict(dict):
    def __getitem__(self, key):
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        if not is_public_function(key, value):
            super().__setitem__(key, value)
            return

        if key not in self:
            super().__setitem__(key, OverloadFunction())
        self[key].append(value)

class Overloaded(type):
    def __prepare__(metacls, cls):
        return OverloadDict()


if __name__ == '__main__':
    class A(metaclass=Overloaded):
        def __init__(self):
            self.x = 1
        def f(self):
            return self.x
        def f(self, x):
            return self.x + x

    a = A()
    print(a.f())
    print(a.f(3))