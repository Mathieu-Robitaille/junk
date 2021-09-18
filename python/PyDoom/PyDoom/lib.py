from math import sqrt
from json import load
from os.path import exists

if not exists('./config.json'):
    raise FileNotFoundError
config = load('./config.json')

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


def subtract(v1, v2):
    return Point(v1.x - v2.x, v1.y - v2.y)


def magnitude(vec):
    return sqrt(vec.x ** 2 + vec.y ** 2)


def dot_product(v1, v2):
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

