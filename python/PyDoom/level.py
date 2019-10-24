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
           "#   #  ## #   #" \
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


def get_north(c, l):
    return l.map[c.id - l.width] if c.id - l.width >= 0 else None


def get_south(c, l):
    return l.map[c.id + l.width] if c.id + l.width <= len(l.map) else None


def get_east(c, l):
    return l.map[c.id + 1] if c.id % l.width is not l.width - 1 else None


def get_west(c, l):
    return l.map[c.id - 1] if c.id % l.width is not 0 else None


def create_wall(c, l, d):
    """
    :param c: cell
    :param l: level obj
    :param d: direction "N, S, E, W"
    :return:
    """
    wall_id = len(l.walls)
    starting = one_d_to_two_d(c.id, l.width)
    ending = (0, 0)
    if d in ("N", "S"):
        ending = starting[0] + 1, starting[1]
    elif d in ("E", "W"):
        ending = starting[0], starting[1] + 1
    l.walls.append((starting, ending))
    return wall_id


def extend_wall(i, l, d):
    """
    :param i: Wall id to work on
    :param l: level obj
    :param d: direction "N, S, E, W"
    :return:
    """
    if d in ("N", "S"):
        l.walls[i] = l.walls[i][1][0] + 1, l.walls[i][1][1]
    elif d in ("E", "W"):
        l.walls[i] = l.walls[i][1][0], l.walls[i][1][1] + 1


def carry_or_create_wall(c, l):
    if c.is_wall is False:
        return

    # Order is N, S, E, W
    neighbors = [get_north(c, l), get_south(c, l),
                 get_east(c, l), get_west(c, l)]

    """
    These are the questions that need to be answered to decide if we create a wall or extend a wall
    We will use a northern wall as an example, this would be a wall segment on the northern face of a cell
    
    Is there a cell to the north that is a wall or None?
    Is there a cell to the east and is it a wall?
    A northern cell would obstruct all visibility of the wall we're evaluating so skip if there is a cell.
    Creating or extending a wall depends on the presence of a cell to the east.
    If there is a cell to the east and that cell has a wall to the north, just take that cell's north wall ID
    Otherwise create a wall ot the north.
    
    """

    # Evaluate the situation for the Northern wall
    if (neighbors[0] is not None and not neighbors[0].is_wall) and neighbors[2] is not None:
        if neighbors[2].is_wall and neighbors[2].walls[0] is not 0:
            extend_wall(neighbors[2].walls[0], l, "N")
            c.walls[0] = neighbors[2].walls[0]
        else:
            c.walls[0] = create_wall(c, l, "N")





class Cell:
    def __init__(self, id, is_wall):
        self.id = id
        self.is_wall = is_wall
        # Order is North, South, East, West
        self.walls = [0, 0, 0, 0]


class Level:
    def __init__(self):
        super().__init__()
        # Width, Height
        self.width = LEVEL_WIDTH
        self.height = LEVEL_HEIGHT

        # Walls are stored as ((startx, starty), (endx, endy)) with the index being the id of the wall
        self.walls = [((0, 0), (0, 0))]
        self.map = create_cells(get_map(self.width, self.height))

    def update(self):
        pass
