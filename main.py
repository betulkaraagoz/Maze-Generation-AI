import pygame
from IDS import *
from UCS import *
from AStar import *
from utils import *
import time
import sys
import timeit

sys.setrecursionlimit(10000)


def main():
    run = True
    n = 357

    width = 1785
    height = 1785

    caption = "Maze {n:d}x{n:d}"
    win = pygame.display.set_mode((width+1, height+1))
    pygame.display.set_caption(caption.format(n=n))
    clock = pygame.time.Clock()
    win.fill((30, 30, 30))

    grid = initCells(win, width, n)
    stack = []
    current = list(grid.nodes)[0]
    start = list(grid.nodes)[0]
    goal = list(grid.nodes)[n*n-1]
    print("maze size: " + str(n))
    while run:
        # clock.tick(60)
        current.visited = True
        for cell in grid.nodes:
            Cell.show(cell)

        #current.highlight()
        neigh_indexs = current.getNeighIndex()
        next_pos = notVisitedNeighs(neigh_indexs, list(grid.nodes))

        if next_pos != -1:
            next_pos.visited = True
            stack.append(current)
            removeWalls(current, next_pos)
            current.possible_ways.append(next_pos)
            next_pos.possible_ways.append(current)
            current = next_pos

        elif stack != []:
            current = stack.pop()

        if stack == []:
            run = False
            t_end = time.time() + 2
            while time.time() < t_end:
                for cell in grid.nodes:
                    Cell.show(cell)

            pygame.display.update()
            print("finished maze generation")
            start_astar = timeit.default_timer()
            pathASTAR = astar(start, goal, "manhattan")
            print("path " + str(len(pathASTAR)))
            stop_astar = timeit.default_timer()
            print("A* with manhattan heuristic found path in " + str(find_significant(stop_astar-start_astar)) + " seconds")
            start_astar = timeit.default_timer()
            pathASTAR = astar(start, goal, "euclidean")
            stop_astar = timeit.default_timer()
            print("A* with euclidean heuristic found path in " + str(find_significant(stop_astar - start_astar)) + " seconds")
            start_ucs = timeit.default_timer()
            pathUCS = ucs(start, goal)
            stop_ucs = timeit.default_timer()
            print("UCS found path in " + str(find_significant(stop_ucs - start_ucs)) + " seconds")
            start_ids = timeit.default_timer()
            pathIDS, depth, expanded = IDDFS(grid, start, goal, 10000)
            stop_ids = timeit.default_timer()
            print("IDS found target in " + str(depth) + " depth for a " + str(n) + "x" + str(n) + " maze by expanding "+ str(expanded) + " nodes")
            print("IDS found path in " + str(find_significant(stop_ids - start_ids)) + " seconds")
            print("The length of the path found is " + str(len(pathASTAR)))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                pygame.quit()

        pygame.display.update()

    pygame.image.save(win, "maze-1-{n:d}x{n:d}.png".format(n=n))
    #wait for 10 seconds to display path
    t_end = time.time() + 2

    while time.time() < t_end:
        for cell in grid.nodes:
            Cell.show(cell)

        if pathASTAR:
            start.highlight_path(pathASTAR[1], None)
            for i in range(len(pathASTAR)):
                prev_node = pathASTAR[i-1]
                solution_node = pathASTAR[i]
                if i == len(pathASTAR)-1:
                    next_node = None
                else:
                    next_node = pathASTAR[i+1]
                solution_node.highlight_path(next_node, prev_node)

        pygame.display.update()

    pygame.image.save(win, "path_of_maze-1-{n:d}x{n:d}.png".format(n=n))

main()
