from math import floor
from random import randint

from globals import *


class Cell:
    def __init__(self, pos):
        # Base Cell class other cells will morph if needed by a search type
        self.id = pos
        self.neighbors = []
        self.visited = True
        # [0] = x, [1] = y
        self.position = (pos % LEVEL_SIZE, floor(pos / LEVEL_SIZE))
        # East and South
        # We do not need to care about all directions on each cell as wither it's neighbors will handle that
        # or it does not have neighbors in that direction
        self.path = [False, False]

    def populate_neighbors(self, cells):
        # Check if the cell has neighbors in each cardinal direction
        # then assigns them as its neighbors or None keeping indexing as an option for referencing
        # direction, ex: north = 0 cell.neighbors[north]
        # (This is not implemented yet. However, it will add an additional layer of clarity to the code)
        north = self.id - LEVEL_SIZE if self.position[1] > 0 else None
        east = self.id + 1 if self.position[0] < LEVEL_SIZE - 1 else None
        south = self.id + LEVEL_SIZE if self.position[1] < LEVEL_SIZE - 1 else None
        west = self.id - 1 if self.position[0] > 0 else None
        self.neighbors = [cells[i] for i in [north, east, south, west] if i is not None]


def create_world():
    cells = [Cell(i) for i in range(LEVEL_SIZE * LEVEL_SIZE)]
    for cell in cells:
        cell.populate_neighbors(cells)
    stack = [cells[0]]
    while stack:
        this_cell = stack[-1]
        this_cell.visited = True
        possible_next_cells = [i for i in this_cell.neighbors if not i.visited and i is not None]
        if len(possible_next_cells) == 0:
            stack.pop()
            continue
        next_cell = possible_next_cells[randint(0, len(possible_next_cells) - 1)]
        if next_cell.id - LEVEL_SIZE == this_cell.id:
            this_cell.path[1] = True
        elif next_cell.id + LEVEL_SIZE == this_cell.id:
            next_cell.path[1] = True
        elif next_cell.id + 1 == this_cell.id:
            next_cell.path[0] = True
        elif next_cell.id - 1 == this_cell.id:
            this_cell.path[0] = True
        stack.append(next_cell)
    for cell in cells:
        if randint(0, 100) > 100 - PATH_CHANCE:
            if randint(0, 100) > PATH_DIRECTION_CHANCE:
                # east
                if cell.position[0] < LEVEL_SIZE - 1:
                    cell.path[0] = True
            else:
                # south
                if cell.position[1] < LEVEL_SIZE - 1:
                    cell.path[1] = True
    return cells


class Level():
    def __init__(self):
        super().__init__()
        # Width, Height
        self.width = 16
        self.height = 12
        self.map = "".join([
            "###############",
            "#     ##### # #",
            "#      #### # #",
            "#       #     #",
            "#          #  #",
            "# ####   ###  #",
            "#          #  #",
            "# #####    #  #",
            "#          #  #",
            "#   #         #",
            "#             #",
            "#  #       #  #",
            "#  ## ### ##  #",
            "#      #      #",
            "###############"
        ])
        # self.map = create_world()

    def update(self):
        pass
