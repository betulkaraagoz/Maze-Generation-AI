from queue import PriorityQueue

def ucs(possible_ways, graph, start, goal):
    visited = set()
    queue = PriorityQueue()
    queue.put((0, start))
    start.g = 0
    path = {}
    path[start.number] = [start]

    while queue:
        cost, node = queue.get()
        if node not in visited:
            visited.add(node)

            if node == goal:
                print("UCS found with cost " + str(cost))
                return path[node.number]

            for i in possible_ways[node.number]:
                if i not in visited:
                    total_cost = cost + 1
                    queue.put((total_cost, i))
                    path[i.number] = path[node.number].copy()
                    path[i.number].append(i)