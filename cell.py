import pygame


class Cell:
    def __init__(self, win, x, y, cellSize, dim, number):
        self.number = number
        self.win = win
        self.x = x * cellSize
        self.y = y * cellSize
        self.xIndex = x
        self.yIndex = y
        self.cellSize = cellSize
        self.cols = dim[0]
        self.rows = dim[1]
        left = True
        top = True
        right = True
        bottom = True
        self.edges = [top, left, bottom, right]
        self.visited = False
        #self.reachable = reachable
        self.parent = None
        # cost to move from the starting cell to this cell
        # #estimation of the cost to move from this cell to the ending cell.
        # f = g + h
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f


    def show(self):
        if self.visited:
            pygame.draw.rect(self.win, (0, 0, 255), (self.x, self.y, self.cellSize, self.cellSize))
        if self.edges[0]:
            pygame.draw.line(self.win, (255, 255, 255), [self.x, self.y], [(self.x + self.cellSize), self.y], 1)
        if self.edges[1]:
            pygame.draw.line(self.win, (255, 255, 255), [self.x, self.y], [self.x, (self.y + self.cellSize)], 1)
        if self.edges[2]:
            pygame.draw.line(self.win, (255, 255, 255), [self.x, (self.y + self.cellSize)],
                             [(self.x + self.cellSize), (self.y + self.cellSize)], 1)
        if self.edges[3]:
            pygame.draw.line(self.win, (255, 255, 255), [(self.x + self.cellSize), (self.y + self.cellSize)],
                             [(self.x + self.cellSize), self.y], 1)

    def highlight(self):
        pygame.draw.rect(self.win, (0, 255, 0), (self.x, self.y, self.cellSize, self.cellSize))

    def highlight_path(self):
        pygame.draw.circle(self.win, (255, 0, 255), (self.x + self.cellSize/2, self.y + self.cellSize/2), self.cellSize/5)

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

    def get_heuristic(self, end):
        """Compute the heuristic value H for a cell.
        Distance between this cell and the ending cell multiply by 10.
        @returns heuristic value H
        """
        return 10 * (abs(self.x - end.x) + abs(self.y - end.y))
