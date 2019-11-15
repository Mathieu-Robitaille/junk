from math import floor
from random import randint, choice
import logger
from globals import *
from timeit import default_timer as timer



def get_map(width, height):
    # Return default test value
    return "###############" \
           "#         #   #" \
           "#       #  #  #" \
           "#        #    #" \
           "#             #" \
           "#   ###   #   #" \
           "#   #     #   #" \
           "#   #  #  #   #" \
           "#   #  #  #   #" \
           "###########   #" \
           "#             #" \
           "#    # ##     #" \
           "#    ###      #" \
           "#             #" \
           "###############"

def get_map2(width, height):
    #
    # Figure out how to override global's LEVEL_WIDTH
    #
    return "##############################" \
           "#                            #" \
           "#                            #" \
           "#                            #" \
           "#                            #" \
           "#           ########         #" \
           "#           #      #         #" \
           "#           #                #" \
           "#           #      #         #" \
           "#           ########         #" \
           "#                            #" \
           "#                            #" \
           "#                            #" \
           "#                            #" \
           "##############################"

def create_cells(level_map):
    # WHO NEEDS READABILITY
    # also the single line solution is 0.0002 seconds slower so....
    # I've included the expanded version of the code for readability
    # r = []
    # for i in range(len(level_map) - 1):
    #     if level_map[i] is '#':
    #         # It's a wall
    #         r.append(Cell(i, is_wall=True))
    #     else:
    #         # Not a wall
    #         r.append(Cell(i, is_wall=False))
    return [Cell(x, True if level_map[x] is '#' else False) for x in range(len(level_map))]


def get_north(c, l):
    return l.map[c.id - l.width] if c.id - l.width >= 0 else None


def get_south(c, l):
    result = None
    try:
        result = l.map[c.id + l.width] if c.id + l.width <= len(l.map) - 1 else None
    except Exception as e:
        print("oh no")
    return result


def get_east(c, l):
    return l.map[c.id + 1] if c.id % l.width is not l.width - 1 else None


def get_west(c, l):
    return l.map[c.id - 1] if c.id % l.width is not 0 else None


def create_wall(c, l, d):
    """
    This creates a wall respective of the face of the cell it is on
    :param c: cell
    :param l: level obj
    :param d: direction "N, S, E, W"
    :return:
    """
    wall_id = len(l.walls)
    starting = one_d_to_two_d(c.id, l.width)
    ending = (0, 0)
    if d == "N":
        ending = starting[0] + 1, starting[1]
    elif d == "S":
        starting = starting[0], starting[1] + 1
        ending = starting[0] + 1, starting[1]
    elif d == "E":
        starting = starting[0] + 1, starting[1]
        ending = starting[0], starting[1] + 1
    elif d == "W":
        ending = starting[0], starting[1] + 1
    l.walls.append(Line(starting, ending))
    return wall_id


def extend_wall(i, l, d):
    """
    :param i: Wall id to work on
    :param l: level obj
    :param d: direction "N, S, E, W"
    :return:
    """
    if d in ("N", "S"):
        l.walls[i].p2.x += 1
    elif d in ("E", "W"):
        l.walls[i].p2.y += 1


def carry_or_create_wall(c, l):
    """
    This function builds a list of line segments we treat as obstacles for actor vision and movement
    or "walls" as normal people call them

    Check readme for more information on how the logic works for this
    :param c:
    :param l:
    :return:
    """

    if c.is_wall is False:
        return

    # Order is N, S, E, W
    north = get_north(c, l)
    south = get_south(c, l)
    east = get_east(c, l)
    west = get_west(c, l)


    # Evaluate the situation for the Northern wall
    if (north is not None and not north.is_wall) and west is not None:
        if west.walls[0] is not 0:
            extend_wall(west.walls[0], l, "N")
            c.walls[0] = west.walls[0]
        else:
            c.walls[0] = create_wall(c, l, "N")

    # Evaluate the Southern wall
    if (south is not None and not south.is_wall) and west is not None:
        if west.walls[1] is not 0:
            extend_wall(west.walls[1], l, "S")
            c.walls[1] = west.walls[1]
        else:
            c.walls[1] = create_wall(c, l, "S")

    # Evaluate the east wall
    if (east is not None and not east.is_wall) and north is not None:
        if north.walls[2] is not 0:
            extend_wall(north.walls[2], l, "E")
            c.walls[2] = north.walls[2]
        else:
            c.walls[2] = create_wall(c, l, "E")

    # Evaluate the west wall
    if (west is not None and not west.is_wall) and north is not None:
        if north.walls[3] is not 0:
            extend_wall(north.walls[3], l, "W")
            c.walls[3] = north.walls[3]
        else:
            c.walls[3] = create_wall(c, l, "W")


class Cell:
    def __init__(self, cell_id, is_wall):
        self.id = cell_id
        self.is_wall = is_wall
        # Order is North, South, East, West
        self.walls = [0, 0, 0, 0]


class Level:
    def __init__(self):
        super().__init__()
        # Width, Height
        self.width = LEVEL_WIDTH
        self.height = LEVEL_HEIGHT

        # Walls are stored as a Line obj with the index being the id of the wall
        self.walls = [Line((0, 0), (0, 0))]
        self.map = create_cells(get_map(self.width, self.height))
        for cell in self.map:
            carry_or_create_wall(cell, self)

    def update(self, frame_time):
        pass
