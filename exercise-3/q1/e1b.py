def dfs(tree):
    index, next = tree
    yield index

    for n in next:
        yield from dfs(n)
