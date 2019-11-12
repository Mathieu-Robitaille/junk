from math import cos, sin, pi, fabs, sqrt, atan2
from timeit import default_timer as timer

import numpy as np
import pygame as pg
import logger
from globals import *


def points_in_circum(offset=0, radius=100, n=100):
    """
    Returns a list of (x, y) points offset from 0, 0 based on self.pos
    These coordinates are the circumference of a circle

    ARGS:
    @ param r = Radius in pixels
    @ param n = number of divisions, meaning the frequency of points along the circumfrence.

    RETURNS:
        List of (x, y) points
    """
    return [((cos(2 * pi / n * x) * radius + offset),
             (sin(2 * pi / n * x) * radius + offset))
            for x in range(0, n + 1)]


def draw(g, s):
    walls = build_z_buffer_walls(g)
    walls.sort(key=lambda Wall: Wall.n_d, reverse=True)
    draw_walls(s, g, walls)
    # draw_sprites(s, cast_list)
    draw_minimap(s, g, walls)


def build_z_buffer_walls(g):
    # The return value, we'll add all walls to be drawn to this list
    z_buffer_walls = []

    pos = g.player.pos

    walls = g.level.walls[1:]

    right_line = Line(
        (pos.x, pos.y),
        get_right_fov_extreme_point(g.player)
    )

    left_line = Line(
        (pos.x, pos.y),
        get_left_fov_extreme_point(g.player)
    )

    for wall in walls:
        # Condense code a bit, if statements were getting long
        pv = point_in_view
        ri = line_intersection(right_line, wall)
        li = line_intersection(left_line, wall)

        # Figure out how to order these dots

        if ri and li:
            z_buffer_walls.append(Wall(li, ri, pos))
            continue

        if ri:
            if pv(wall.p1, g.player):
                p = wall.p1
            else:
                p = wall.p2
            z_buffer_walls.append(Wall(p, ri, pos))
            continue

        if li:
            p = wall.p1 if pv(wall.p1, g.player) else wall.p2
            z_buffer_walls.append(Wall(li, p, pos))
            continue

        if not ri and not li:
            # check if its still in view
            if pv(wall.p1, g.player) and pv(wall.p2, g.player):
                z_buffer_walls.append(Wall(wall.p1, wall.p2, pos))

    return z_buffer_walls


def draw_walls(s, g, w):
    # Draw each cast as a vertical line to be matched up with the next cast for
    # smoooooth walls

    # Draw the sky
    pg.draw.rect(s, (135, 206, 235),
                 (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT / 2))

    # Draw the floor so its prettier
    pg.draw.rect(s, (0, 64, 0),
                 (0, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT / 2))

    c = g.player
    pos = g.player.pos

    left_point = get_left_fov_extreme_point(c)
    right_point = get_right_fov_extreme_point(c)
    left_line = Line(pos, left_point)
    right_line = Line(pos, right_point)

    for i in w:
        try:
            x1 = get_x_coordinate(c, i.p1, left_line, right_line)
            x2 = get_x_coordinate(c, i.p2, left_line, right_line)
            coordinates = (
                (x2, i.ceiling_p2),
                (x1, i.ceiling_p1),
                (x1, i.floor_p1),
                (x2, i.floor_p2)
            )
            color = (i.color_p1, i.color_p1, i.color_p1)
            pg.draw.polygon(s, color, coordinates, 0)
        except IndexError as e:  # e here incase I want to use it later,
            logger.log("you done it now boy")
        except TypeError:
            logger.log("points err", coordinates)


def draw_sprites(s, c):
    """
    For sprite drawing we'll need to build a "Z buffer" ordered by distance to the player, drawing each item in the list
    in reverse order (farthest thing first, closest thing last)
    :param s: surface to draw things to
    :param c: cast list, do I really need this????
    :return: nothing
    """
    pass


def draw_minimap(s, g, w):
    """
    DEBUG TOOL
    :param s:
    :param g:
    :param c:
    :return:
    """

    pg.draw.rect(s, pg.Color("Black"),
                 (SCREEN_WIDTH - (LEVEL_WIDTH * LEVEL_CELL_SPACING),
                  0,
                  LEVEL_WIDTH * LEVEL_CELL_SPACING,
                  LEVEL_HEIGHT * LEVEL_CELL_SPACING))

    # Translate the current player's position to the mini map structure
    player_pos = (int(RENDER_MINI_MAP_OFFSET + (g.player.pos.x * LEVEL_CELL_SPACING)),
                  int(g.player.pos.y * LEVEL_CELL_SPACING))

    # Draw the player fov
    ra = get_right_minimap_extreme(player_pos, g.player.angle, g.player.fov, 200)
    la = get_left_minimap_extreme(player_pos, g.player.angle, g.player.fov, 200)
    pg.draw.line(s, pg.Color("Blue"), player_pos, ra)
    pg.draw.line(s, pg.Color("Blue"), player_pos, la)

    # Player
    pg.draw.circle(s, pg.Color("red"), player_pos, 1)

    for wall in g.level.walls:
        start = (int(RENDER_MINI_MAP_OFFSET + (wall.p1.x * LEVEL_CELL_SPACING)),
                 int(wall.p1.y * LEVEL_CELL_SPACING))
        end = (int(RENDER_MINI_MAP_OFFSET + (wall.p2.x * LEVEL_CELL_SPACING)),
               int(wall.p2.y * LEVEL_CELL_SPACING))
        pg.draw.line(s, pg.Color("Green"), start, end)
    for wall in w:
        try:
            ls = (int(RENDER_MINI_MAP_OFFSET + (wall.p1.x * LEVEL_CELL_SPACING)),
                  int(wall.p1.y * LEVEL_CELL_SPACING))
            le = (int(RENDER_MINI_MAP_OFFSET + (wall.p2.x * LEVEL_CELL_SPACING)),
                  int(wall.p2.y * LEVEL_CELL_SPACING))
            pg.draw.line(s, pg.Color("Red"), ls, le)
        except IndexError:
            logger.log("index error")
        except TypeError as e:
            logger.log("Type error")


"""
Below are the supporting functions 
These all need error checking, type checking, and comments
"""


def get_x_coordinate(entity, point, l, r):
    """
    This is really bad and needs to get re-worked
    :param entity: Current player, camera
    :param point: Point we're evaluating
    :param l: Current player's left fov max (Line)
    :param r: Current player's right fov max (Line)
    :return: x coordinate normalised for the screen
    """
    if fuzzy_is_on_line(point, l):
        return 0
    elif fuzzy_is_on_line(point, r):
        return SCREEN_WIDTH
    else:
        ang = get_angle(entity, l.p2, point)
        ang2 = get_angle(entity, r.p2, point)
        # get_angle returns a different value at different distances.
        # I'm not sure how to solve this issue without the current get _angle code
        # so a quick patch that works is to get the angle from both sides of the fov
        # and add them together since this will always be the maximum for that distance
        return normalize(ang,
                         0, ang + ang2,
                         0, SCREEN_WIDTH)



def is_on_line(p, l):
    """
    Checks if a point is on a line
    :param p: Point to check of type Point
    :param l: Line to be evaluated of type Line
    :return: bool, True if the point is on the line, else false
    """
    d = distance_to_point
    d1 = d(p, l.p1) + d(p, l.p2)
    d2 = d(l.p1, l.p2)
    if d1 == d2:
        return True
    return False


def fuzzy_is_on_line(p, l):
    """
    Checks if a point is on a line
    :param p: Point to check of type Point
    :param l: Line to be evaluated of type Line
    :return: bool, True if the point is on the line, else false
    """
    d = distance_to_point
    d1 = d(p, l.p1) + d(p, l.p2)
    d2 = d(l.p1, l.p2)
    # Pad it because floating point accuracy
    if d1 - 0.0003 <= d2 <= d1 + 0.0003:
        return True
    return False


def line_intersection(l1, l2):
    """
    Takes two line objects and checks if they intersect, if they do return the x, y coordinate of the intersection
    else return False

    Using the following resource I was able to build a faster implementation of this than using the
    shapely library which was far too slow for these purposes (This is better but possibly not the final solution)
    http://paulbourke.net/geometry/pointlineplane/
    :param l1: A Line object
    :param l2: A line object
    :return: x, y or False
    """
    d = (l2.p2.y - l2.p1.y) * (l1.p2.x - l1.p1.x) \
        - \
        (l2.p2.x - l2.p1.x) * (l1.p2.y - l1.p1.y)
    if d == 0:
        return False

    a = (l2.p2.x - l2.p1.x) * (l1.p1.y - l2.p1.y) \
        - \
        (l2.p2.y - l2.p1.y) * (l1.p1.x - l2.p1.x)
    b = (l1.p2.x - l1.p1.x) * (l1.p1.y - l2.p1.y) \
        - \
        (l1.p2.y - l1.p1.y) * (l1.p1.x - l2.p1.x)

    ra = a / d
    rb = b / d

    if 0 <= ra <= 1 and 0 <= rb <= 1:
        x = l1.p1.x + (ra * (l1.p2.x - l1.p1.x))
        y = l1.p1.y + (ra * (l1.p2.y - l1.p1.y))
        return Point(x, y)
    else:
        return False


def calc_ceiling(d):
    return (SCREEN_HEIGHT / 2.0) - SCREEN_HEIGHT / d


def calc_floor(c):
    return SCREEN_HEIGHT - c


def point_in_view(p, c):
    """
    # https://www.geeksforgeeks.org/check-whether-a-given-point-lies-inside-a-triangle-or-not/
    # im a big ol 2 head
    Checks if point (p) is in character (c) vision
    :param p: Point object
    :param c: Character/Entity object with angle, fov, and pos values
    :return: True/False
    """
    l = get_left_fov_extreme_point(c)
    r = get_right_fov_extreme_point(c)
    if is_inside(c.pos, l, r, p):
        return True
    else:
        return False


def is_inside(a, b, c, p):
    def area(x1, y1, x2, y2, x3, y3):
        return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)
    # Calculate area of triangle ABC
    abc = area(a.x, a.y, b.x, b.y, c.x, c.y)

    # Calculate area of triangle PBC
    pbc = area(p.x, p.y, b.x, b.y, c.x, c.y)

    # Calculate area of triangle PAC
    pac = area(a.x, a.y, p.x, p.y, c.x, c.y)

    # Calculate area of triangle PAB
    pab = area(a.x, a.y, b.x, b.y, p.x, p.y)

    # Check if sum of pbc, pbc and pab
    # is same as A
    r = pbc + pac + pab
    if r - 0.5 <= abc <= r + 0.5:
        return True
    else:
        return False


# Standardise angles for easy maths
def get_right_fov_extreme_ang(c):
    """
    :param c: Entity object
    :return:
    """
    return c.angle + c.fov / 2


def get_left_fov_extreme_ang(c):
    """
    :param c: Entity object
    :return:
    """
    return c.angle - c.fov / 2


def get_right_fov_extreme_point(c, d=RENDER_DEPTH):
    """
    :param c: Entity object
    :param d: distance to offset the point
    :return: Point obj at the right extreme of the characters FOV
    """
    return Point(c.pos.x - d * sin(c.angle + c.fov / 2),
                 c.pos.y + d * cos(c.angle + c.fov / 2))


def get_left_fov_extreme_point(c, d=RENDER_DEPTH):
    """
    :param c: Entity object
    :param d: distance to offset the point
    :return: Point obj at the left extreme of the characters FOV
    """
    return Point(c.pos.x - d * sin(c.angle - c.fov / 2),
                 c.pos.y + d * cos(c.angle - c.fov / 2))


def get_right_minimap_extreme(p, a, f, d=200):
    """
    :param p: position Point obj
    :param a: angle in radians
    :param f: FOV angle in radians
    :param d: distance to offset the point
    :return: tuple (x, y) of the right FOV extreme
    """
    return int(p[0] - d * sin(a + f / 2)), int(p[1] + d * cos(a + f / 2))


def get_left_minimap_extreme(p, a, f, d=200):
    """
    :param p: position Point obj
    :param a: angle in radians
    :param f: FOV angle in radians
    :param d: distance to offset the point
    :return: tuple (x, y) of the left FOV extreme
    """
    return int(p[0] - d * sin(a - f / 2)), int(p[1] + d * cos(a - f / 2))


def get_angle(entity, fov_enpoint, point):
    """
    :param entity: Entity we're measuring from
    :param fov_enpoint: Fov arm endpoint
    :param point: Point we're getting the angle to
    :return: Radians
    """
    a = np.array([entity.pos.x, entity.pos.y])
    b = np.array([fov_enpoint.x, fov_enpoint.y])
    c = np.array([point.x, point.y])
    ba = b - a
    bc = b - c
    cos_ang = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    return np.arccos(cos_ang) * 10


