from math import floor
from random import randint, choice
import logger
from globals import *


def get_map(width, height):
    # Return default test value
    return "###############" \
           "#             #" \
           "#             #" \
           "#             #" \
           "#             #" \
           "#   #     #   #" \
           "#   #     #   #" \
           "#   #     #   #" \
           "#   #     #   #" \
           "#   #  #  #   #" \
           "#             #" \
           "#             #" \
           "#             #" \
           "#             #" \
           "###############"


def create_cells(level_map):
    # WHO NEEDS READABILITY
    # result = []
    # for i in level_map:
    #     if level_map[i] is '#':
    #         # It's a wall
    #         result.append(Cell(i, is_wall=True))
    #     else:
    #         # Not a wall
    #         result.append(Cell(i, is_wall=False))
    # return result
    return [Cell(x, True if level_map[x] is '#' else False) for x in range(len(level_map))]


def get_north(cell, w):
    return cell - w if cell - w >= 0 else -1


def get_south(cell, w, h):
    return cell + w if cell + w <= w * h else -1


def get_east(cell, w):
    return cell + 1 if cell % w is not w - 1 else -1


def get_west(cell, w):
    return cell - 1 if cell % w is not 0 else 1


def edge_detect(level_map):
    # Returns a list of walls in form [(X1, Y1), (X2, Y2), (Xn, Yn)]
    for cell in level_map:
        if cell.is_wall:
            # Carry or create walls here
            continue
    pass


class Cell:
    def __init__(self, id, is_wall):
        self.id = id
        self.is_wall = is_wall
        # Order is North, South, East, West
        self.walls = [-1, -1, -1, -1]


class Level:
    def __init__(self):
        super().__init__()
        # Width, Height
        self.width = LEVEL_WIDTH
        self.height = LEVEL_HEIGHT
        self.map = create_cells(get_map(self.width, self.height))

    def update(self):
        pass
