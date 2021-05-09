from math import sqrt

import pygame


class Cell:
    def __init__(self, win, x, y, cellSize, dim, number):
        self.number = number #unique number used for key
        self.win = win
        self.x = x * cellSize
        self.y = y * cellSize
        self.xIndex = x
        self.yIndex = y
        self.cellSize = cellSize
        self.cols = dim[0]
        self.rows = dim[1]
        self.edges = [True, True, True, True]
        self.visited = False
        self.priority = 0
        self.possible_ways = []
        self.g = 0 #cost from start to this node, used in UCS
        self.f = 0 #total cost for A*
        self.h = 0 #cost of heuristic

    def __lt__(self, other):
        #print(self.g)
        #print(other.g)
        return self.priority < other.priority


    def show(self):
        if self.visited:
            pygame.draw.rect(self.win, (255, 255, 255), (self.x, self.y, self.cellSize, self.cellSize))
        if self.edges[0]:
            pygame.draw.line(self.win, (0, 0, 0), [self.x, self.y], [(self.x + self.cellSize), self.y], 1)
        if self.edges[1]:
            pygame.draw.line(self.win, (0, 0, 0), [self.x, self.y], [self.x, (self.y + self.cellSize)], 1)
        if self.edges[2]:
            pygame.draw.line(self.win, (0, 0, 0), [self.x, (self.y + self.cellSize)],
                             [(self.x + self.cellSize), (self.y + self.cellSize)], 1)
        if self.edges[3]:
            pygame.draw.line(self.win, (0, 0, 0), [(self.x + self.cellSize), (self.y + self.cellSize)],
                             [(self.x + self.cellSize), self.y], 1)

    def highlight(self):
        pygame.draw.rect(self.win, (255, 0, 255), (self.x, self.y, self.cellSize, self.cellSize))

    def highlight_path(self, next_node, prev_node):
        if next_node is not None:
            if next_node.number > self.number:
                if next_node.yIndex == self.yIndex:
                    #next is on the right
                    pygame.draw.line(self.win, (255, 0, 255), [self.x + self.cellSize/2, (self.y + self.cellSize/2)],
                                     [(self.x + self.cellSize), (self.y + self.cellSize/2)], 3)

                elif next_node.xIndex == self.xIndex:
                    #next is below
                    pygame.draw.line(self.win, (255, 0, 255), [self.x + self.cellSize/2, (self.y + self.cellSize/2)],
                                     [(self.x + self.cellSize/2), (self.y + self.cellSize)], 3)


            else:
                if next_node.yIndex == self.yIndex:
                    # next is on the left
                    pygame.draw.line(self.win, (255, 0, 255), [self.x + self.cellSize/2, (self.y + self.cellSize/2)],
                                     [(self.x), (self.y + self.cellSize/2)], 3)

                elif next_node.xIndex == self.xIndex:
                    # next is above
                    pygame.draw.line(self.win, (255, 0, 255), [self.x + self.cellSize/2, (self.y + self.cellSize/2)],
                                     [(self.x + self.cellSize/2), (self.y)], 3)

        if prev_node is not None:
            if prev_node.number > self.number:
                if prev_node.yIndex == self.yIndex:
                    #prev is on the right
                    pygame.draw.line(self.win, (255, 0, 255), [self.x + self.cellSize/2, (self.y + self.cellSize/2)],
                                     [(self.x + self.cellSize), (self.y + self.cellSize/2)], 3)

                elif prev_node.xIndex == self.xIndex:
                    #prev is below
                    pygame.draw.line(self.win, (255, 0, 255), [self.x + self.cellSize/2, (self.y + self.cellSize/2)],
                                     [(self.x + self.cellSize/2), (self.y + self.cellSize)], 3)

            else:
                if prev_node.yIndex == self.yIndex:
                    # prev is on the left
                    pygame.draw.line(self.win, (255, 0, 255), [self.x + self.cellSize/2, (self.y + self.cellSize/2)],
                                     [(self.x), (self.y + self.cellSize/2)], 3)

                elif prev_node.xIndex == self.xIndex:
                    # prev is above
                    pygame.draw.line(self.win, (255, 0, 255), [self.x + self.cellSize/2, (self.y + self.cellSize/2)],
                                     [(self.x + self.cellSize/2), (self.y)], 3)

        if next_node is None:
            pygame.draw.circle(self.win, (255, 0, 0), (self.x + self.cellSize / 2, self.y + self.cellSize / 2),
                               self.cellSize / 5)
        if prev_node is None:
            pygame.draw.circle(self.win, (0, 255, 0), (self.x + self.cellSize / 2, self.y + self.cellSize / 2),
                               self.cellSize / 5)

    def getNeighIndex(self):
        top = self.getIndex(self.xIndex, self.yIndex - 1)
        left = self.getIndex(self.xIndex - 1, self.yIndex)
        bottom = self.getIndex(self.xIndex, self.yIndex + 1)
        right = self.getIndex(self.xIndex + 1, self.yIndex)

        return [top, left, bottom, right]

    def getIndex(self, x, y):
        if x < 0 or x > self.cols - 1 or y < 0 or y > self.rows - 1:
            return -1
        else:
            return x + y * self.cols

    def get_euclidean_heuristic(self, goal):
        dx = abs(self.xIndex - goal.xIndex)
        dy = abs(self.yIndex - goal.yIndex)
        return sqrt(dx * dx + dy * dy)

    def get_manhattan_heuristic(self, goal):
        dx = abs(self.xIndex - goal.xIndex)
        dy = abs(self.yIndex - goal.yIndex)
        return dx + dy