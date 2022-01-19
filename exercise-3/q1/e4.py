class MultiDict:
    def __init__(self):
        self.dict = {}

    def __str__(self):
        return str(self.dict)

    def __repr__(self):
        return repr(self.dict)

    def __getitem__(self, key):
        return self.dict[key][0]
    
    def __setitem__(self, key, val):
        if key in self.dict:
            self.dict[key].append(val)
        else:
            self.dict[key] = [val]

    def __delitem__(self, key):
        entry = self.dict[key]
        entry.pop(0)
        if len(entry) == 0:
            del self.dict[key]

    def __contains__(self, key):
        return key in self.dict

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.dict == other.dict

    def __bool__(self):
        return bool(self.dict)

    def __len__(self):
        return len(self.dict)

    def __iter__(self):
        return iter(self.dict)

    def get_all(self, key):
        return self.dict[key]

    def delete_all(self, key):
        del self.dict[key]



md = MultiDict()
md['x'] = 1
md['x'] = 2
print(md['x'])
print(md.get_all('x'))
del md['x']
print(md['x'])
md.delete_all('x')
print(md)