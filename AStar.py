from queue import PriorityQueue


def astar(possible_ways, graph, start, goal):
    visited = set()
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
        cost, current = frontier.get()
        expanded += 1
        if current not in visited:
            visited.add(current)

            if current == goal:
                print("A* found with cost " + str(cost) + " by expanding " + str(expanded) + " nodes")
                return path[current.number]

            for next in possible_ways[current.number]:
                if next not in visited:
                    total_cost = cost + 1
                    new_cost = cost_so_far[current] + total_cost
                    if next not in cost_so_far or new_cost < cost_so_far[next]:
                        cost_so_far[next] = new_cost
                        priority = new_cost + next.get_manhattan_heuristic(goal)
                        frontier.put((priority, next))
                        came_from[next] = current
                        path[next.number] = path[current.number].copy()
                        path[next.number].append(next)
