import pygame
from IDS import *
from UCS import *
from AStar import *
from utils import *
import time
import sys
import timeit

sys.setrecursionlimit(3000)


def main():
    run = True
    n = 10

    width = 1000
    height = 1000

    caption = "Maze {n:d}x{n:d}"
    win = pygame.display.set_mode((width+1, height+1))
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
        # for cell in grid.nodes:
        #     Cell.show(cell)

        #current.highlight()
        neigh_indexs = current.getNeighIndex()
        print(current.getIndex(current.xIndex, current.yIndex))
        #print(neigh_indexs)
        next_pos = notVisitedNeighs(neigh_indexs, list(grid.nodes))
        #print(possible_ways)
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
            t_end = time.time() + 2
            # while time.time() < t_end:
            #     for cell in grid.nodes:
            #         Cell.show(cell)
            #
            # pygame.display.update()
            print("finished maze generation")
            start_astar = timeit.default_timer()
            pathASTAR = astar(possible_ways, grid, list(grid.nodes)[0], list(grid.nodes)[n*n-1], "manhattan")
            stop_astar = timeit.default_timer()
            print("A* with manhattan heuristic found path in " + str(find_significant(stop_astar-start_astar)) + " seconds")
            start_astar = timeit.default_timer()
            pathASTAR = astar(possible_ways, grid, list(grid.nodes)[0], list(grid.nodes)[n*n-1], "euclidean")
            stop_astar = timeit.default_timer()
            print("A* with euclidean heuristic found path in " + str(find_significant(stop_astar - start_astar)) + " seconds")
            start_ucs = timeit.default_timer()
            pathUCS = ucs(possible_ways, grid, list(grid.nodes)[0], list(grid.nodes)[n*n-1])
            stop_ucs = timeit.default_timer()
            print("UCS found path in " + str(find_significant(stop_ucs - start_ucs)) + " seconds")
            start_ids = timeit.default_timer()
            pathIDS, depth, expanded = IDDFS(possible_ways, grid, list(grid.nodes)[0], list(grid.nodes)[n*n-1], 5000)
            stop_ids = timeit.default_timer()
            print("IDS found target in " + str(depth) + " depth for a " + str(n) + "x" + str(n) + " maze by expanding "+ str(expanded) + " nodes")
            print("IDS found path in " + str(find_significant(stop_ids - start_ids)) + " seconds")
            print("The length of the path found is " + str(len(pathASTAR)))


        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         quit()
        #         pygame.quit()
        #
        # pygame.display.update()

    pygame.image.save(win, "maze-1-{n:d}x{n:d}.png".format(n=n))
    #wait for 10 seconds to display path
    t_end = time.time() + 2

    # while time.time() < t_end:
    #     for cell in grid.nodes:
    #         Cell.show(cell)

    if pathASTAR:
        list(grid.nodes)[0].highlight_path(pathASTAR[1], None)
        for i in range(len(pathASTAR)):
            prev_node = pathASTAR[i-1]
            solution_node = pathASTAR[i]
            if i == len(pathASTAR)-1:
                next_node = None
            else:
                next_node = pathASTAR[i+1]
            solution_node.highlight_path(next_node, prev_node)

        #pygame.display.update()

    pygame.image.save(win, "path_of_maze-1-{n:d}x{n:d}.png".format(n=n))

    #t_end = time.time() + 10
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
