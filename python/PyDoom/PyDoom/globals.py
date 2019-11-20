from math import sqrt

VERSION = "0.0.4"


#
# All constants must begin with const type then constname
# EX: RENDER_ for constants used by the render manager
#


#
# Pygame init constants
#
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800


#
# World generation constants
#
NORTH = 0
SOUTH = 1
EAST = 2
WEST = 3
LEVEL_WIDTH = 15
LEVEL_HEIGHT = 15
LEVEL_SIZE = LEVEL_WIDTH * LEVEL_WIDTH
LEVEL_PATH_LENGTH_MIN = 3   # Random number, may need some tuning
LEVEL_PATH_LENGTH_MAX = 10  # Random number, may need some tuning
LEVEL_PATH_CHANCE = 100
LEVEL_PATH_DIRECTION_CHANCE = 50
LEVEL_CELL_SPACING = 10
LEVEL_PATH_OFFSET = 10

#
# Room size and shape logic consts
#
# The average size of rooms by way on number of cells in the room
ROOM_SIZE = 60
ROOM_CHANCE = 0.6

ROOM_COUNT_MAX = 10  # int(LEVEL_SIZE / (ROOM_SIZE / 3) / ROOM_CHANCE) + 1
ROOM_COUNT_MIN = 5   # int(ROOM_COUNT_MAX / 1.5)


#
# Menu globals
#
MENU_SPACING = 40



#
# Render constants
#
RENDER_DEPTH = 30
RENDER_WALL_SIZE = 2.5
# This is the divisor for ray casting, a larger number means more deg between rays

RENDER_MINI_MAP_OFFSET = SCREEN_WIDTH - (LEVEL_WIDTH * LEVEL_PATH_OFFSET)

#
# Screen type "enums"
#
SCREEN_MENU = 0
SCREEN_OPTIONS = 1
SCREEN_GAME = 2

MENU_OPTIONS_MAIN = ["New Game", "Options", "Exit"]
MENU_OPTIONS_OPTION = ["Graphics : {}x{}".format(SCREEN_WIDTH, SCREEN_HEIGHT), "Volume : 100", "Back"]

#
# Entity "enums"
#
TEAM_GAEA = 0
TEAM_PLAYER = 1
TEAM_ENEMY = 2

#
# Image utility globals
#
IU_ASSET_DIR = "PyDoom/assets"


#
# Text options
#
FONT = "freesansbold.ttf"

#
# Logging constants
#
LOGGING_DIR = "logs"


#
# Data types and global functions
# Should probably go into its own file "SaSM"?? Structures and supporting methods?
#

def two_d_to_one_d(xy, w):
    """

    :param xy:
    :param w:
    :return:
    """
    return int(xy[1]) * w + int(xy[0])


def one_d_to_two_d(cid, w):
    """

    :param cid:
    :param w:
    :return:
    """
    return cid % w, int(cid / w)


def distance_to_point(a, b):
    """
    A simple point to point distance measure tool
    :param a: x, y coords of point a
    :param b: x, y coords of point a
    :return: float: distance between a and b
    """
    if isinstance(a, Point) and isinstance(b, Point):
        return sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2)
    return sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)


def normalize(val, old_min, old_max, new_min, new_max):
    old_range = old_max - old_min
    new_range = new_max - new_min
    return ((val - old_min) * new_range) / old_range + new_min


def sub(v1, v2):
    return Point(v1.x - v2.x, v1.y - v2.y)


def mag(vec):
    return sqrt(vec.x ** 2 + vec.y ** 2)


def dot(v1, v2):
    return v1.x * v2.x + v1.y * v2.y


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "{} {}".format(self.x, self.y)


class Line:
    def __init__(self, p1, p2):
        self.p1 = Point(*p1) if not isinstance(p1, Point) else p1
        self.p2 = Point(*p2) if not isinstance(p2, Point) else p2

    def __str__(self):
        return "{} {}".format(self.p1, self.p2)


class Wall:
    def __init__(self, p1, p2, player_pos):
        self.p1 = p1
        self.p2 = p2
        self.p1_d = distance_to_point(player_pos, p1)
        self.p2_d = distance_to_point(player_pos, p2)
        self.n_d = distance_to_point(player_pos, Point((p2.x + p1.x) / 2, (p2.y + p1.y) / 2))
        self.ceiling_p1 = (SCREEN_HEIGHT / 2.0) - SCREEN_HEIGHT / self.p1_d
        self.ceiling_p2 = (SCREEN_HEIGHT / 2.0) - SCREEN_HEIGHT / self.p2_d
        self.floor_p1 = SCREEN_HEIGHT - self.ceiling_p1
        self.floor_p2 = SCREEN_HEIGHT - self.ceiling_p2
        self.color_p1 = 255 - normalize(distance_to_point(p1, player_pos), 0, RENDER_DEPTH, 0, 255)
        self.color_p2 = 255 - normalize(distance_to_point(p2, player_pos), 0, RENDER_DEPTH, 0, 255)

    def __str__(self):
        # return str("{} {}".format(self.p1, self.p2))
        return str(self.n_d)

    def __lt__(self, other):
        if isinstance(other, Wall):
            return self.n_d < self.n_d
        else:
            raise Exception("Not instance of wall")

    def __gt__(self, other):
        if isinstance(other, Wall):
            return self.n_d > self.n_d
        else:
            raise Exception("Not instance of wall")


#
#
#

