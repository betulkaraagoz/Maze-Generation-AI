from queue import PriorityQueue

def ucs(start, goal):
    visited = set()
    queue = PriorityQueue()
    queue.put(start, 0)
    start.g = 0
    start.priority = 0

    path = {}
    path[start.number] = [start]
    expanded = 0

    while queue:
        node = queue.get()

        if node not in visited:
            visited.add(node)
            expanded += 1

            if node == goal:
                print("UCS found with cost " + str(node.g) + " by expanding " + str(expanded) + " nodes")
                return path[node.number]

            for i in node.possible_ways:
                if i not in visited:
                    total_cost = node.g + 1
                    i.priority = total_cost
                    i.g = total_cost
                    queue.put(i, total_cost)
                    path[i.number] = path[node.number].copy()
                    path[i.number].append(i)