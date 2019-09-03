from math import floor, sqrt
from random import randint
# I'm pretty sure wildcard imports are bad?
from mazeglobals import *


class Cell:
    def __init__(self, pos):
        # Base Cell class other cells will morph if needed by a search type
        self.id = pos
        self.neighbors = []
        self.is_start = False
        self.is_end = False
        self.visited = False
        self.parent = None
        # [0] = x, [1] = y
        self.position = (pos % MAZE_WIDTH, floor(pos / MAZE_WIDTH))
        self.draw_position = (-1, -1)
        # East and South
        # We do not need to care about all directions on each cell as wither it's neighbors will handle that
        # or it does not have neighbors in that direction
        self.path = [False, False]

    def populate_neighbors(self, cells):
        # Check if the cell has neighbors in each cardinal direction
        # then assigns them as its neighbors or None keeping indexing as an option for referencing
        # direction, ex: north = 0 cell.neighbors[north]
        # (This is not implemented yet. However, it will add an additional layer of clarity to the code)
        north = self.id - MAZE_WIDTH if self.position[1] > 0 else None
        east = self.id + 1 if self.position[0] < MAZE_WIDTH - 1 else None
        south = self.id + MAZE_WIDTH if self.position[1] < MAZE_HEIGHT - 1 else None
        west = self.id - 1 if self.position[0] > 0 else None
        self.neighbors = [cells[i] for i in [north, east, south, west] if i is not None]


class World:
    def __init__(self):
        self.cells = [Cell(i) for i in range(MAZE_WIDTH * MAZE_HEIGHT)]
        self.start = 0 # randint(0, MAZE_WIDTH * MAZE_HEIGHT)
        self.end = MAZE_WIDTH * MAZE_HEIGHT - 1 # randint(0, MAZE_WIDTH * MAZE_HEIGHT)
        self.cells[self.start].is_start = True
        self.cells[self.end].is_end = True
        for cell in self.cells:
            cell.populate_neighbors(self.cells)
            cell.draw_position = (cell.position[0] * DRAW_OFFSET + sqrt(PATH_WIDTH),
                                  cell.position[1] * DRAW_OFFSET + sqrt(PATH_WIDTH))

    def update(self, stack):
        this_cell = stack[-1]
        this_cell.visited = True
        possible_next_cells = [i for i in this_cell.neighbors if not i.visited and i is not None]
        if len(possible_next_cells) == 0:
            stack.pop()
            return
        next_cell = possible_next_cells[randint(0, len(possible_next_cells) - 1)]
        if next_cell.id - MAZE_WIDTH == this_cell.id:
            this_cell.path[1] = True
        elif next_cell.id + MAZE_WIDTH == this_cell.id:
            next_cell.path[1] = True
        elif next_cell.id + 1 == this_cell.id:
            next_cell.path[0] = True
        elif next_cell.id - 1 == this_cell.id:
            this_cell.path[0] = True
        stack.append(next_cell)

    def random_paths(self):
        for cell in self.cells:
            if randint(0, 100) > PATH_CHANCE:
                if randint(0, 100) > PATH_DIRECTION_CHANCE:
                    # east
                    if not cell.position[0] + 1 == MAZE_WIDTH:
                        cell.path[0] = True
                else:
                    # south
                    if not cell.position[1] + 1 == MAZE_HEIGHT:
                        cell.path[1] = True
        return True
