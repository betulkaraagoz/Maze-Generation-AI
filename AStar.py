from queue import PriorityQueue


def astar(start, goal, heuristic):
    frontier = PriorityQueue()
    frontier.put(start, 0)

    start_heuristic = 0
    if heuristic == "manhattan":
        start_heuristic = start.get_manhattan_heuristic(goal)
    elif heuristic == "euclidean":
        start_heuristic = start.get_euclidean_heuristic(goal)

    start.g = 0
    start.h = start_heuristic
    start.f = start.f + start.g
    start.priority = start.f

    path = {}
    path[start.number] = [start]

    cost_so_far = dict()
    cost_so_far[start] = 0

    expanded = 0

    while not frontier.empty():
        current = frontier.get()
        expanded += 1

        if current == goal:
            print("A* found with cost " + " by expanding " + str(expanded) + " nodes")
            return path[current.number]

        for next in current.possible_ways:
            next.g = current.g + 1

            if heuristic == "manhattan":
                heuristic_value = next.get_manhattan_heuristic(goal)
            elif heuristic == "euclidean":
                heuristic_value = next.get_euclidean_heuristic(goal)
            next.h = heuristic_value

            new_cost = next.g + next.h
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic_value
                next.priority = priority
                frontier.put(next, priority)
                path[next.number] = path[current.number].copy()
                path[next.number].append(next)
