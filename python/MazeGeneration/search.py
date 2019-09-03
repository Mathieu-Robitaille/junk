import heapq
import pygame

from math import floor, sqrt
from world import Cell as WorldCell
# I'm pretty sure wildcard imports are bad?
from mazeglobals import *


class Cell(WorldCell):
    def __init__(self, c):
        # Override the world cells as we require additional data
        # other algos will not need
        #
        # g = cost to move from the starting cell to this cell
        # h = estimation of the cost to move from this cell to end cell
        # f = g + h
        super().__init__(c.id)
        self.path = c.path
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        # We need to create a less than comparison as the heapq will use it to order
        # each cell. Without it the heapq has no idea how to compare the cells
        if isinstance(other, Cell):
            return self.f < other.f


class Search:
    def __init__(self, world, screen):
        self.world = world
        self.cells = self.world.cells
        self.screen = screen
        self.opened = []
        self.closed = set()
        self.solved = False
        self.path = []
        self.end = self.cells[self.world.end]
        self.start = self.cells[self.world.start]

    def get_reachable(self, cell):
        """
        This iterates over all the neighbors of this cell and evaluates if a path could
        be made between them
        :param cell: The current cell being evaluated
        :return: A list of cardinal directions in clockwise order starting at north,
                    if the cell is not reachable it returns (False, None) for that cell
        """
        north = south = east = west = (False, None)
        for neighbor in cell.neighbors:
            if neighbor.id == cell.id - MAZE_WIDTH:
                north = (True if neighbor.path[1] else False, neighbor)
            elif neighbor.id == cell.id + MAZE_WIDTH:
                south = (True if cell.path[1] else False, neighbor)
            elif neighbor.id == cell.id - 1:
                west = (True if neighbor.path[0] else False, neighbor)
            elif neighbor.id == cell.id + 1:
                east = (True if cell.path[0] else False, neighbor)
        return [north, east, south, west]

    def get_path(self):
        # Iterates through the gathered cells by jumping to its parent
        # constructing a list of cells on the path between the start and end
        cell = self.end
        path = [cell]
        while cell.parent is not self.start:
            cell = cell.parent
            path.append(cell)
        path.append(self.start)
        self.path = path

    def draw_cell(self, cell, color=WHITE, update=False):
        pygame.draw.rect(self.screen, color,
                         (cell.draw_position[0],
                          cell.draw_position[1],
                          PATH_WIDTH, PATH_WIDTH))
        if update:
            pygame.display.update()

    def update_cell(self, cell, neighbor):
        if neighbor.parent is None:
            neighbor.parent = cell

    def draw(self):
        for cell in self.cells:
            if cell in self.closed:
                color = GREY
                if cell is self.start:
                    color = BLUE
                if cell is self.end:
                    color = RED
                self.draw_cell(cell, color)
        if self.path:
            divisions = 255 / len(self.path)
            color = RED
            for cell in self.path:
                if cell.parent is None:
                    continue
                color = (color[0] - divisions if color[0] - divisions > 0 else 0, 0,
                         color[2] + divisions if color[2] + divisions < 255 else 255)
                pygame.draw.line(self.screen, color,
                                 (cell.draw_position[0] + PATH_WIDTH / 2,
                                  cell.draw_position[1] + PATH_WIDTH / 2),
                                 (cell.parent.draw_position[0] + PATH_WIDTH / 2,
                                  cell.parent.draw_position[1] + PATH_WIDTH / 2),
                                 floor(WALL_WIDTH / 2))


class StarSearch(Search):
    def __init__(self, world, screen):
        super().__init__(world, screen)
        # Init the search, we need to rebuild the set of cells as they need more info stored in them
        heapq.heapify(self.opened)
        self.cells = [Cell(c) for c in self.world.cells]
        # This may not be the best way to do this.
        self.end = self.cells[self.world.end]
        self.start = self.cells[self.world.start]
        for cell in self.cells:
            cell.populate_neighbors(self.cells)
            cell.draw_position = (cell.position[0] * DRAW_OFFSET + sqrt(PATH_WIDTH),
                                  cell.position[1] * DRAW_OFFSET + sqrt(PATH_WIDTH))
        heapq.heappush(self.opened, (self.start.f, self.start))

    def get_heuristic(self, cell):
        """
        Calculate the heuristic value H for a cell: dist between this cell and the ending cell x 10
        :param cell: the cell of which to calculate the heuristic
        :returns heuristic value:
        """
        return 10 * (abs(cell.position[1] - self.end.position[1]) + abs(cell.position[0] - self.end.position[0]))

    def update_cell(self, adj, cell):
        """
        Updates a cells' heuristic and parent
        :param adj: The cell adjacent to the current cell to be updated
        :param cell: The current cell being evaluated
        :return: None
        """
        adj.g = cell.g + 10
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g

    def update(self):
        """
        The big worky worky bit
        Iterates over each cell, working with the most efficient path via the heapq sorting the
        lowest costing (f) cell to the top to be evaluated next.
        """
        if not self.path:
            f, cell = heapq.heappop(self.opened)
            self.closed.add(cell)
            if cell is self.end:
                self.get_path()
                self.solved = True
            self.draw_cell(cell, BLUE)
            neighbors = self.get_reachable(cell)
            for reachable, neighbor in neighbors:
                if reachable and neighbor not in self.closed:
                    if (neighbor.f, neighbor) in self.opened:
                        if neighbor.g > cell.g + 10:
                            self.update_cell(neighbor, cell)
                    else:
                        # Something isnt right here....?
                        self.update_cell(neighbor, cell)
                        heapq.heappush(self.opened, (neighbor.f, neighbor))
                    self.draw_cell(neighbor, GREEN)
        else:
            return


class FloodFill(Search):
    def __init__(self, world, screen):
        super().__init__(world, screen)
        self.opened = [self.start]

    def update(self):
        if not self.path:
            cell = self.opened.pop(0)
            self.closed.add(cell)
            self.draw_cell(cell, BLUE)
            if cell is self.end:
                self.get_path()
                self.solved = True
            for reachable, neighbor in self.get_reachable(cell):
                if reachable and neighbor not in self.closed:
                    self.update_cell(cell, neighbor)
                    self.draw_cell(neighbor, GREEN)
                    self.opened.append(neighbor)
