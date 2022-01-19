class TransformDict:
    def __init__(self, transform):
        self.transform = transform
        self.dict = {}

    def __str__(self):
        return str(self.dict)

    def __repr__(self):
        return repr(self.dict)

    def __getitem__(self, key):
        return self.dict[self.transform(key)]
    
    def __setitem__(self, key, val):
        self.dict[self.transform(key)] = val

    def __delitem__(self, key):
        key = self.transform(key)
        del self.dict[key]

    def __contains__(self, key):
        return self.transform(key) in self.dict

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.dict == other.dict

    def __bool__(self):
        return bool(self.dict)

    def __len__(self):
        return len(self.dict)

    def __iter__(self):
        return iter(self.dict)


td = TransformDict(lambda key: key.lower())
td['FOO'] = 1
td['foo'] = 2
print(td['Foo'])
td['BAR'] = 3
print(td)
