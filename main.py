from collections import deque
from queue import PriorityQueue

import pygame
from cell import Cell
from IDS import *
from utils import *
import time
import copy


def main():
    run = True
    width = 1000
    height = 1000
    n = 10
    caption = "Maze {n:d}x{n:d}"
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption.format(n=n))
    clock = pygame.time.Clock()
    win.fill((30, 30, 30))
    possible_ways = dict()

    grid = initCells(win, width, height, n, possible_ways)
    stack = []
    current = list(grid.nodes)[0]
    current.g = 0

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
            next_pos.g = current.g + 1
            stack.append(current)
            removeWalls(current, next_pos)
            possible_ways[current.number].append(next_pos)
            possible_ways[next_pos.number].append(current)
            current = next_pos

        elif stack != []:
            current = stack.pop()

        if stack == []:
            run = False
            path = ucs(possible_ways, grid, list(grid.nodes)[0], list(grid.nodes)[99])
            #path, depth = IDDFS(possible_ways, grid, list(grid.nodes)[0], list(grid.nodes)[399], 5000)
            #print("IDS found target in " + str(depth) + " depth for a " + str(n) + "x" + str(n) + " maze")

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


main()
