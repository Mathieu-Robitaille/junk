from math import cos, sin, pi, fabs, sqrt, atan2
from timeit import default_timer as timer

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
    draw_walls(s, g, walls)
    # draw_sprites(s, cast_list)
    draw_minimap(s, g, walls)


def build_z_buffer_walls(g):
    # The return value, we'll add all walls to be drawn to this list
    z_buffer_walls = []

    # localise these vars as it's more clear plus python accesses local variables faster
    # Expand player position for clarity
    player_pos_x = g.player.pos.x
    player_pos_y = g.player.pos.y
    player_angle = g.player.angle
    player_fov = g.player.fov

    walls = g.level.walls[1:]

    right_angle = (player_angle + player_fov / 2)
    left_angle = (player_angle - player_fov / 2)

    right_line = Line(
        (player_pos_x, player_pos_y),
        (player_pos_x - sin(right_angle) * RENDER_DEPTH,
         player_pos_y + cos(right_angle) * RENDER_DEPTH)
    )

    left_line = Line(
        (player_pos_x, player_pos_y),
        (player_pos_x + sin(left_angle) * RENDER_DEPTH,
         player_pos_y - cos(left_angle) * RENDER_DEPTH)
    )

    for wall in walls:
        w = wall
        # Condense code a bit, if statements were getting long
        pv = point_in_view
        right_intersect = line_intersection(right_line, wall)
        left_intersection = line_intersection(left_line, wall)
        if right_intersect:
            # Check which point is in player vision
            p = wall.p1 if pv(wall.p1, g.player) else wall.p2
            w = Wall(p, right_intersect, g.player.pos)
        if left_intersection:
            if right_intersect:
                w = Wall(right_intersect, left_intersection, g.player.pos)
            else:
                p = wall.p1 if pv(wall.p1, g.player) else wall.p2
                w = Wall(p, left_intersection, g.player.pos)
        if not right_intersect and not left_intersection:
            # check if its still in view
            if pv(wall.p1, g.player) and pv(wall.p2, g.player):
                w = Wall(wall.p1, wall.p2, g.player.pos)
        if isinstance(w, Wall):
            # Yes, this will append all walls interacted with into this buffer
            # Either find a way to find the side of a wall facing the player so we do not
            # draw both sides of a wall, or say heck it and draw it anyways.
            # the previous solution would draw like 1200 polygons to the screen and that didnt
            # seem to be the big slowdown so lets leave it for now.
            z_buffer_walls.append(w)
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

    left_angle = (g.player.angle - g.player.fov / 2)
    right_angle = (g.player.angle + g.player.fov / 2)

    for i in w:
        try:
            t1 = get_angle(i.p1, g.player.pos)
            t2 = get_angle(i.p2, g.player.pos)
            x1 = normalize(t1, left_angle, right_angle, 0, SCREEN_WIDTH)
            x2 = normalize(t2, left_angle, right_angle, 0, SCREEN_WIDTH)
            coordinates = (
                (x1, i.ceiling_p1),
                (x1, i.floor_p1),
                (x2, i.ceiling_p2),
                (x2, i.floor_p2)
            )
            color = (i.color_p1, i.color_p1, i.color_p1)
            pg.draw.polygon(s, color, coordinates, 0)
        except IndexError as e:  # e here incase I want to use it later,
            logger.log("you done it now boy")


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
    player_pos = (int(SCREEN_WIDTH - (g.player.pos.x * LEVEL_CELL_SPACING)),
                  int(g.player.pos.y * LEVEL_CELL_SPACING))

    # Draw the player fov
    player_right_aim = (player_pos[0] - 20 * sin(g.player.angle + g.player.fov / 2),
                        player_pos[1] + 20 * cos(g.player.angle + g.player.fov / 2))
    player_left_aim = (player_pos[0] - 20 * sin(g.player.angle - g.player.fov / 2),
                       player_pos[1] + 20 * cos(g.player.angle - g.player.fov / 2))
    pg.draw.line(s, pg.Color("Red"), player_pos, player_left_aim)
    pg.draw.line(s, pg.Color("Red"), player_pos, player_right_aim)

    # Player
    pg.draw.circle(s, pg.Color("red"), player_pos, 1)
    for wall in g.level.walls:
        start = (int(SCREEN_WIDTH - (wall.p1.x * LEVEL_CELL_SPACING)),
                 int(wall.p1.y * LEVEL_CELL_SPACING))
        end = (int(SCREEN_WIDTH - (wall.p2.x * LEVEL_CELL_SPACING)),
               int(wall.p2.y * LEVEL_CELL_SPACING))
        pg.draw.line(s, pg.Color("Green"), start, end)
    for wall in w:
        try:
            ls = wall.p1
            le = wall.p2
            ls = (int(SCREEN_WIDTH - (ls.x * LEVEL_CELL_SPACING)),
                  int(ls.y * LEVEL_CELL_SPACING))
            le = (int(SCREEN_WIDTH - (le.x * LEVEL_CELL_SPACING)),
                  int(le.y * LEVEL_CELL_SPACING))
            pg.draw.line(s, pg.Color("Red"), ls, le)
        except IndexError:
            logger.log("index error")
        except TypeError as e:
            logger.log("Type error")


def distance_to_point(a, b):
    """
    A simple point to point distance measure tool
    :param a: x, y coords of point a
    :param b: x, y coords of point a
    :return: float: distance between a and b
    """
    return sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)


def is_on_line(p, l):
    """
    Checks if a point is on a line
    :param p: Point to check of type Point
    :param l: Line to be evaluated of type Line
    :return: bool, True if the point is on the line, else false
    """
    # Create local version of this function for shorter code allowing it to be read
    # on lower res screens easier
    d = distance_to_point
    if d(p, l.p1) + d(p, l.p2) == d(*l):
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


def normalize(val, old_min, old_max, new_min, new_max):
    old_range = old_max - old_min
    new_range = new_max - new_min
    return ((val - old_min) * new_range) / old_range + new_min


def calc_ceiling(d):
    return (SCREEN_HEIGHT / 2.0) - SCREEN_HEIGHT / d


def calc_floor(c):
    return SCREEN_HEIGHT - c


def get_angle(p1, p2):
    return atan2(p1.y - p2.y, p1.x - p2.x)


def point_in_view(p, c):
    """
    Checks if point (p) is in character (c) vision
    :param p: Point object
    :param c: Character/Entity object with angle, fov, and pos values
    :return: True/False
    """
    right_angle = (c.angle + c.fov / 2)
    left_angle = (c.angle - c.fov / 2)
    t = atan2(c.pos.y - p.y, c.pos.x - p.x)
    if left_angle <= t <= right_angle:
        return True
    return False
