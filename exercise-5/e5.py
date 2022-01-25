import sys

class MyModule:
    def __repr__(self):
        return 'magic module'

    def __call__(self, arg):
        return arg

    def __getitem__(self, key):
        return key

# Anything in python can be overriden. Everything is just a dictionary.
# Duck typing means it doesn't matter what class this is replaced with.
sys.modules[__name__] = MyModule()