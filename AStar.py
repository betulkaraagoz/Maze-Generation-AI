from queue import PriorityQueue


def astar(possible_ways, graph, start, goal, heuristic):
    frontier = PriorityQueue()
    frontier.put((0, start))

    start.g = 0
    path = {}
    path[start.number] = [start]

    came_from = dict()
    cost_so_far = dict()
    came_from[start] = None
    cost_so_far[start] = 0
    expanded = 0

    while not frontier.empty():
        other, current = frontier.get()
        expanded += 1

        if current == goal:
            print("A* found with cost " + " by expanding " + str(expanded) + " nodes")
            return path[current.number]

        for next in possible_ways[current.number]:
            total_cost = current.g + 1
            new_cost = cost_so_far[current] + total_cost
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                next.g = total_cost
                cost_so_far[next] = new_cost
                if heuristic == "manhattan":
                    heuristic_value = next.get_manhattan_heuristic(goal)
                elif heuristic == "euclidean":
                    heuristic_value = next.get_euclidean_heuristic(goal)
                priority = new_cost + heuristic_value
                frontier.put((priority, next))
                came_from[next] = current
                path[next.number] = path[current.number].copy()
                path[next.number].append(next)
