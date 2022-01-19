def bfs(tree):
    queue = [tree]
    for index, next in queue:
        # Add all of the nodes underneath this one to the back of the queue.
        for n in next:
            queue.append(n)
        yield index
