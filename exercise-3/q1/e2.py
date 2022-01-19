import pathlib

class Entry:
    def __init__(self, path):
        self.path = path
        self.recurse_into = True 

    def skip(self):
        self.recurse_into = False

    def depth(self):
        ppath = self.path
        depth = 0
        while ppath != pathlib.Path(self.path.root):
            ppath = ppath.parent
            depth += 1
        return depth

    @property
    def name(self):
        return str(self.path.name)

    @property
    def type(self):
        return "directory" if self.path.is_dir() else "file"


def walk(root):
    # DFS of files starting from root.
    # root - resolved pathlib.Path
    # I don't understand what order he wants in tests so I wrote my own here 
    # and I'm satisfied with the results.
    for path in [x.resolve() for x in root.iterdir() if x.is_file()]:
        yield Entry(path)

    for path in [x.resolve() for x in root.iterdir() if x.is_dir()]:
        e = Entry(path)
        yield e

        if e.recurse_into and path.is_dir():
            yield from walk(path)


root = pathlib.Path('/home/matan/Documents/gittick-course/exercise-3/q1').resolve()
for e in walk(root.resolve()):
    root_entry = Entry(root)
    leading_space = ' ' * (e.depth() - root_entry.depth()) * 4
    print(f'{leading_space}{e.name} ({e.type})')
    if e.name == '.pytest_cache':
        e.skip()