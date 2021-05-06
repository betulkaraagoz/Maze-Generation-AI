expanded = 0


def DLS(possible_ways, graph, src, target, depth, path):
    global expanded
    current = path[len(path) - 1]

    if current.xIndex == target.xIndex and current.yIndex == target.yIndex:
        return path, expanded

    # If reached the maximum depth, stop recursing.
    if depth <= 0:
        return None

    # Recur for all the vertices adjacent to this vertex
    adjacents = possible_ways[src.number]

    for node in adjacents:
        if node in path:
            continue
        new_path = list(path)
        new_path.append(node)
        expanded += 1
        result = DLS(possible_ways, graph, node, target, depth - 1, new_path)
        if result is not None:
            return result, expanded


def IDDFS(possible_ways, graph, src, target, maxDepth):
    global expanded
    for depth in range(maxDepth):
        path = DLS(possible_ways, graph, src, target, depth, [src])
        if path is None:
            continue
        return path, depth, expanded
