import threading

def make_sync(cls, fname, f):
    def sync(*args, **kwargs):
        with cls.lock:
            return f(*args, **kwargs)
    setattr(cls, fname + '_sync', sync)

def make_safe(cls, fname, f):
    def safe(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            pass
    setattr(cls, fname + '_safe', safe)

class Extended(type):
    def __init__(cls, name, bases, attrs):
        cls.lock = threading.Lock()
        for key, value in attrs.items():
            if not callable(value) or key.startswith('__'):
                continue

            make_sync(cls, key, value)
            make_safe(cls, key, value)


if __name__ == '__main__':
    class A(metaclass=Extended):
        def __init__(self):
            self.x = 1
        
        def f(self):
            self.x += 1

        def g(self):
            raise TypeError

    a = A()
    a.f_sync()
    a.g_safe()