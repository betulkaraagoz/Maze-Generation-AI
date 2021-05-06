import pygame
from IDS import *
from UCS import *
from AStar import *
from utils import *
import time
import sys

sys.setrecursionlimit(3000)


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
            pathASTAR = astar(possible_ways, grid, list(grid.nodes)[0], list(grid.nodes)[399])
            pathUCS = ucs(possible_ways, grid, list(grid.nodes)[0], list(grid.nodes)[399])
            pathIDS, depth, expanded = IDDFS(possible_ways, grid, list(grid.nodes)[0], list(grid.nodes)[399], 5000)
            print("IDS found target in " + str(depth) + " depth for a " + str(n) + "x" + str(n) + " maze by expanding "
                  + str(expanded) + " nodes")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                pygame.quit()

        pygame.display.update()

    #wait for 10 seconds to display path
    t_end = time.time() + 10

    while time.time() < t_end:
        for cell in grid.nodes:
            Cell.show(cell)

        if pathASTAR:
            list(grid.nodes)[0].highlight_path(pathASTAR[1])
            for i in range(len(pathASTAR)-1):
                solution_node = pathASTAR[i]
                next_node = pathASTAR[i+1]
                solution_node.highlight_path(next_node)

        pygame.display.update()

    t_end = time.time() + 10

    # print("after A*")
    #
    # while time.time() < t_end:
    #     for cell in grid.nodes:
    #         Cell.show(cell)
    #
    #     if pathUCS:
    #         list(grid.nodes)[0].highlight_path()
    #         for solution_node in pathUCS:
    #             solution_node.highlight_path()
    #
    #     pygame.display.update()
    #
    # t_end = time.time() + 10
    # print("after UCS")
    #
    # while time.time() < t_end:
    #     for cell in grid.nodes:
    #         Cell.show(cell)
    #
    #     if pathIDS:
    #         list(grid.nodes)[0].highlight_path()
    #         for solution_node in pathIDS:
    #             solution_node.highlight_path()
    #
    #     pygame.display.update()

main()
