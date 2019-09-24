from math import floor
from random import randint

from globals import *


class Cell:
    def __init__(self, pos, width, height):
        # Base Cell class other cells will morph if needed by a search type
        self.id = pos
        self.neighbors = []
        self.visited = True
        self.level_width = width
        self.level_height = height


        # [0] = x, [1] = y
        self.position = (pos % self.level_width, floor(pos / self.level_width))

        # Added expanded position variables for ease of use, We're keeping self.position
        # since it allows us to use old code without rewriting it immediately (This will need
        # to be re written)
        # TODO: Remove cell.position in favor of cell.x and cell.y for clarity of code
        self.x = self.position[0]
        self.y = self.position[1]

        # We need the corners of the cell so we can find the edges of the cell and path
        # This is NOT the value that will be drawn, this WILL be passed off to a datastructure in
        # the render manager that will handle screen orientation for us
        # as such we leave it all empty
        self.top_wall_id = 0
        self.bottom_wall_id = 0
        self.left_wall_id = 0
        self.right_wall_id = 0

        # Edges in order of North, South, East, and West
        self.edges = [False, False, False, False]

        # East and South
        # We do not need to care about all directions on each cell as wither it's neighbors will handle that
        # or it does not have neighbors in that direction
        # TODO: maybe rethink this logic as it may be favorable for edge detection
        self.path = [False, False]

    def populate_neighbors(self, cells):
        # Check if the cell has neighbors in each cardinal direction
        # then assigns them as its neighbors or None keeping indexing as an option for referencing
        # direction, ex: north = 0 cell.neighbors[north]
        # (This is not implemented yet. However, it will add an additional layer of clarity to the code)
        north = self.id - self.level_width if self.position[1] > 0 else None
        east = self.id + 1 if self.position[0] < self.level_width - 1 else None
        south = self.id + self.level_width if self.position[1] < self.level_height - 1 else None
        west = self.id - 1 if self.position[0] > 0 else None
        self.neighbors = [cells[i] for i in [north, east, south, west] if i is not None]


def create_world(width, height):
    cells = [Cell(i, width, height) for i in range(width * height)]
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
        if next_cell.id - width == this_cell.id:
            this_cell.path[1] = True
        elif next_cell.id + width == this_cell.id:
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
                if cell.position[0] < width - 1:
                    cell.path[0] = True
            else:
                # south
                if cell.position[1] < height - 1:
                    cell.path[1] = True
    return cells


class Level():
    def __init__(self):
        super().__init__()
        # Width, Height
        self.width = LEVEL_WIDTH
        self.height = LEVEL_HEIGHT
        self.map = create_world(self.width, self.height)

    def update(self):
        pass
