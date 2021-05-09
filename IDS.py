expanded = 0


def DLS(graph, src, target, depth, path):
    global expanded
    current = path[len(path) - 1]

    if current.xIndex == target.xIndex and current.yIndex == target.yIndex:
        return path, expanded

    # If reached the maximum depth, stop recursing.
    if depth <= 0:
        return None

    # Recur for all the vertices adjacent to this vertex
    adjacents = src.possible_ways

    for node in adjacents:
        if node in path:
            continue
        new_path = list(path)
        new_path.append(node)
        expanded += 1
        result = DLS(graph, node, target, depth - 1, new_path)
        if result is not None:
            return result, expanded


def IDDFS(graph, src, target, maxDepth):
    global expanded
    for depth in range(maxDepth):
        path = DLS(graph, src, target, depth, [src])
        if path is None:
            continue
        return path, depth, expanded
