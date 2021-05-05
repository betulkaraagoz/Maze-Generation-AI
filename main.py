from collections import deque
import pygame
from cell import Cell
import random as r
import networkx as nx
import time


def main():
    run = True
    width = 1000
    height = 1000
    n = 20
    caption = "Maze {n:d}x{n:d}"
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption.format(n=n))
    clock = pygame.time.Clock()
    win.fill((30, 30, 30))
    possible_ways = dict()

    grid = initCells(win, width, height, n, possible_ways)
    stack = []
    current = list(grid.nodes)[0]



    while run:
        # clock.tick(60)
        current.visited = True
        for cell in grid.nodes:
            Cell.show(cell)

        current.highlight()
        neigh_indexs = current.getNeighIndex()
        next_pos = notVisitedNeighs(neigh_indexs, list(grid.nodes))

        if next_pos != -1:
            next_pos.visited = True
            stack.append(current)
            removeWalls(current, next_pos)
            possible_ways[current.number].append(next_pos)
            possible_ways[next_pos.number].append(current)
            current = next_pos

        elif stack != []:
            current = stack.pop()

        if stack == []:
            run = False
            path, depth = IDDFS(possible_ways, grid, list(grid.nodes)[0], list(grid.nodes)[399], 1000)
            print("IDS found target in " + str(depth) + " depth")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                pygame.quit()

        pygame.display.update()

    #wait for 10 seconds to display path
    t_end = time.time() + 30

    while time.time() < t_end:
        for cell in grid.nodes:
            Cell.show(cell)

        if path:
            list(grid.nodes)[0].highlight_path()
            for solution_node in path:
                solution_node.highlight_path()

        pygame.display.update()


def initCells(win, width, height, n, possible_ways):
    G = nx.Graph()
    counter = 0

    cols, rows = (n, n)
    cell_size = width / n

    for x in range(rows):
        for y in range(cols):
            counter += 1
            G.add_node(node_for_adding=Cell(win, y, x, cell_size, (cols, rows), counter))
            possible_ways[counter] = []
            #grid.append(Cell(win, y, x, cell_size, (cols, rows)))

    return G


def notVisitedNeighs(l, grid):
    possible_moves = []

    for index in l:
        if index == -1:
            del (index)
        try:
            if grid[index].visited is False:
                possible_moves.append(grid[index])
        except:
            continue

    try:
        return r.choice(possible_moves)
    except:
        return -1


def removeWalls(current, next_pos):
    xVal = current.xIndex - next_pos.xIndex

    if xVal == 1:
        current.edges[1] = False
        next_pos.edges[3] = False
    elif xVal == -1:
        current.edges[3] = False
        next_pos.edges[1] = False

    yVal = current.yIndex - next_pos.yIndex

    if yVal == 1:
        current.edges[0] = False
        next_pos.edges[2] = False
    elif yVal == -1:
        current.edges[2] = False
        next_pos.edges[0] = False


def get_cell(grid, height, x, y):
    """Returns a cell from the cells list.
    @param x cell x coordinate
    @param y cell y coordinate
    @returns cell
    """
    return grid.cells[x * height + y]


def update_cell(adj, cell):
    """Update adjacent cell.
    @param adj adjacent cell to current cell
    @param cell current cell being processed
    """
    adj.g = cell.g + 10
    adj.h = Cell.get_heuristic(adj)
    adj.parent = cell
    adj.f = adj.h + adj.g


def DLS(possible_ways, graph, src, target, depth, path):
    current = path[len(path)-1]
    #print(path)

    if current.xIndex == target.xIndex and current.yIndex == target.yIndex:
        return path

    # If reached the maximum depth, stop recursing.
    if depth <= 0:
        return None

    # Recur for all the vertices adjacent to this vertex
    adjacents = possible_ways[src.number]

    # if src in adjacents:
    #      adjacents.remove(src)

    for node in adjacents:
        if node in path:
            continue
        new_path = list(path)
        new_path.append(node)
        result = DLS(possible_ways, graph, node, target, depth - 1, new_path)
        if result is not None:
            return result


def IDDFS(possible_ways, graph, src, target, maxDepth):
    for depth in range(maxDepth):
        path = DLS(possible_ways, graph, src, target, depth, [src])
        if path is None:
            continue

        return path, depth











# def iterative_deepening_dfs(possible_ways, graph, start, goal):
#         prev_iter_visited, depth = [], 0
#         while True:
#             traced_path, visited = depth_limited_search(possible_ways, graph, start, goal, depth)
#             if traced_path or len(visited) == len(prev_iter_visited): return traced_path
#             else: prev_iter_visited = visited; depth += 1
#
#
# def depth_limited_search(possible_ways, graph, start, goal, limit=-1):
#     print('Depth limit =', limit)
#     found, fringe, visited, came_from = False, deque([(0, start)]), set([start]), {start: None}
#     print('{:11s} | {}'.format('Expand Node', 'Fringe'))
#     print('--------------------')
#     print('{:11s} | {}'.format('-', start))
#     while not found and len(fringe):
#         depth, current = fringe.pop()
#         print('{:11s}'.format(current), end=' | ')
#         if current == goal: found = True; break
#         if limit == -1 or depth < limit:
#             for node in self.neighbors(current):
#                 if node not in visited:
#                     visited.add(node); fringe.append((depth + 1, node))
#                     came_from[node] = current
#         print(', '.join([n for _, n in fringe]))
#     if found: print(); return came_from, visited
#     else: print('No path from {} to {}'.format(start, goal)); return None, visited



def getAllNeighbors(grid, cell):
    adjacents = []
    neighsIndices = Cell.getNeighIndex(cell)

    for i in neighsIndices:
        adjacents.append(grid[i])

    return adjacents


def notNeighs(l, grid):
    possible_moves = []

    for index in l:
        if index == -1:
            del (index)
        else:
            possible_moves.append(grid[index])

    return possible_moves


main()
