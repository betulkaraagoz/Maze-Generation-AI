import math

from cell import Cell
import random as r
import networkx as nx

def initCells(win, width, n):
    G = nx.Graph()
    counter = 0

    cols, rows = (n, n)
    cell_size = width / n

    for x in range(rows):
        for y in range(cols):
            G.add_node(node_for_adding=Cell(win, y, x, cell_size, (cols, rows), counter))
            counter += 1

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


def find_significant(number):
    return round(number, 4 - int(math.floor(math.log10(abs(number)))) - 1)
