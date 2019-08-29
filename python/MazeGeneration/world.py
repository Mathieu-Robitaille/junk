from math import floor, sqrt
from random import randint


class Cell:
    def __init__(self, pos, maze_width):
        # Base Cell class other cells will morph if needed by a search type
        self.id = pos
        self.neighbors = []
        self.is_start = False
        self.is_end = False
        self.visited = False
        # [0] = x, [1] = y
        self.position = (pos % maze_width, floor(pos / maze_width))
        self.draw_position = (-1, -1)
        # East and South
        # We do not need to care about all directions on each cell as wither it's neighbors will handle that
        # or it does not have neighbors in that direction
        self.path = [False, False]

    def populate_neighbors(self, w, h, cells):
        # Check if the cell has neighbors in each cardinal direction
        # then assigns them as its neighbors or None keeping indexing as an option for referencing
        # direction, ex: north = 0 cell.neighbors[north]
        # (This is not implemented yet. However, it will add an additional layer of clarity to the code)
        north = self.id - w if self.position[1] > 0 else None
        east = self.id + 1 if self.position[0] < w - 1 else None
        south = self.id + w if self.position[1] < h - 1 else None
        west = self.id - 1 if self.position[0] > 0 else None
        self.neighbors = [cells[i] for i in [north, east, south, west] if i is not None]


class World:
    def __init__(self, maze_width, maze_height, wall_width, path_width):
        self.cells = [Cell(i, maze_width) for i in range(maze_width * maze_height)]
        self.maze_height = maze_height
        self.maze_width = maze_width
        self.wall_width = wall_width
        self.path_width = path_width
        self.start = 0  # randint(0, maze_width * maze_height)
        self.end = maze_width * maze_height - 1  # randint(0, maze_width * maze_height)
        self.cells[self.start].is_start = True
        self.cells[self.end].is_end = True
        self.config_cells()

    def config_cells(self):
        for cell in self.cells:
            cell.populate_neighbors(self.maze_width, self.maze_height, self.cells)
            cell.draw_position = (cell.position[0] * (self.wall_width + self.path_width) + sqrt(self.path_width),
                                  cell.position[1] * (self.wall_width + self.path_width) + sqrt(self.path_width))

    def update(self, stack):
        this_cell = stack[-1]
        this_cell.visited = True
        possible_next_cells = [i for i in this_cell.neighbors if not i.visited and i is not None]
        if len(possible_next_cells) == 0:
            stack.pop()
            return
        next_cell = possible_next_cells[randint(0, len(possible_next_cells) - 1)]
        if next_cell.id - self.maze_width == this_cell.id:
            this_cell.path[1] = True
        elif next_cell.id + self.maze_width == this_cell.id:
            next_cell.path[1] = True
        elif next_cell.id + 1 == this_cell.id:
            next_cell.path[0] = True
        elif next_cell.id - 1 == this_cell.id:
            this_cell.path[0] = True
        stack.append(next_cell)
