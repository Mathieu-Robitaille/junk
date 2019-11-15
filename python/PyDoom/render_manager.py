"""
This module is responsible for taking data from a game object, then translating it
into a visual representation of that data.
"""

from math import cos, sin, pi

import numpy as np
import pygame as pg
import logger
from globals import SCREEN_WIDTH, SCREEN_HEIGHT, LEVEL_WIDTH, LEVEL_HEIGHT, \
    LEVEL_CELL_SPACING, RENDER_MINI_MAP_OFFSET, RENDER_DEPTH, Wall, Line, Point, \
    normalize, distance_to_point


def points_in_circum(offset=0, radius=100, n=100):
    """
    Returns a list of (x, y) points offset from 0, 0 based on self.pos
    These coordinates are the circumference of a circle
    ##### Very old code currently unused #####
    ARGS:
    @ param r = Radius in pixels
    @ param n = number of divisions, meaning the frequency of points along the circumference.

    RETURNS:
        List of (x, y) points
    """
    return [((cos(2 * pi / n * x) * radius + offset),
             (sin(2 * pi / n * x) * radius + offset))
            for x in range(0, n + 1)]


def draw(game, surface):
    """
    The governor for the general order of things being drawn to the game screen
    Eventually there will be a "Z Buffer" handling the draw order for all objects,
    allowing sprites/actors to be partially behind walls
    :param game: The game object
    :param surface: The screen
    """
    # Build collision
    walls = build_z_buffer_walls(game)
    # Rough sort of walls based on their normals
    # (Generally a wall with a further normal will be obscured by others
    #  so it should be drawn first)
    walls.sort(key=lambda wall: wall.n_d, reverse=True)
    draw_walls(surface, game, walls)
    draw_actors(surface, game, walls)
    # Debugging tool,will not be in "release"
    draw_minimap(surface, game, walls)


def build_z_buffer_walls(game):
    """
    Build Wall objects based on the player's Field of View,
    Using this we can build walls by checking where if any
    Intersections occur at the extremes of the player fov,
    if there are then we use that point in the construction of an
    obstacle for the player's vision
    :param game: Game object
    :return:
    """
    # The return value, we'll add all walls to be drawn to this list
    z_buffer_walls = []

    # Localise player pos for shorter more concise code
    pos = game.player.pos

    # The first wall is a garbage wall so get rid of it
    walls = game.level.walls[1:]

    # Right and left line intersection tools
    right_line = Line(
        pos,
        get_right_fov_extreme_point(game.player)
    )
    left_line = Line(
        pos,
        get_left_fov_extreme_point(game.player)
    )

    # Create a local version of this func just for shorter more readable code
    pv = point_in_view

    # If Render distance is exceeded there is a bug where it creates a wall when it should not
    for wall in walls:
        # Condense code a bit, if statements were getting long
        ri = line_intersection(right_line, wall)
        li = line_intersection(left_line, wall)

        # If we're intersecting on the left and right extremes of player fov that means
        #   we already have the corners of the wall to be drawn
        if ri and li:
            z_buffer_walls.append(Wall(li, ri, pos))
            continue

        # If only the right fov extreme intersects then select one of the existing wall end points
        # This is where the bug is as it's assuming RENDER_DISTANCE is larger then the level
        # Could pretty easily be fixedby extending the point_in_view distance or ignoring the wall
        if ri:
            if pv(game.player, wall.p1):
                p = wall.p1
            else:
                p = wall.p2
            z_buffer_walls.append(Wall(p, ri, pos))
            continue
        # Same as above but for the left
        if li:
            p = wall.p1 if pv(game.player, wall.p1) else wall.p2
            z_buffer_walls.append(Wall(li, p, pos))
            continue

        # If there are no intersections but the wall is still in view that means it's
        # an "island" and must be completely in view, just get the whole thing
        if not ri and not li:
            # check if its still in view
            if pv(game.player, wall.p1) and pv(game.player, wall.p2):
                z_buffer_walls.append(Wall(wall.p1, wall.p2, pos))

    return z_buffer_walls


def draw_walls(surface, game, walls):
    """

    :param surface:
    :param game:
    :param walls:
    :return:
    """

    # Draw the sky and floor, makes things prettier
    pg.draw.rect(surface, (135, 206, 235),
                 (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT / 2))
    pg.draw.rect(surface, (0, 64, 0),
                 (0, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT / 2))

    # localise the player var for condensed code
    c = game.player

    left_point = get_left_fov_extreme_point(c)
    left_line = Line(c.pos, left_point)
    right_point = get_right_fov_extreme_point(c)
    right_line = Line(c.pos, right_point)

    for wall in walls:
        try:
            x1 = get_x_coordinate(c, wall.p1, left_line, right_line)
            x2 = get_x_coordinate(c, wall.p2, left_line, right_line)
            coordinates = (
                (x2, wall.ceiling_p2),
                (x1, wall.ceiling_p1),
                (x1, wall.floor_p1),
                (x2, wall.floor_p2)
            )
            color = (wall.color_p1, wall.color_p1, wall.color_p1)
            pg.draw.polygon(surface, color, coordinates)
        except TypeError as e:
            # This exception is not really needed
            logger.log("There has been an exception : ", e)


def draw_actors(surface, game, walls):
    """
    For actor drawing we'll need to build a "Z buffer" ordered by distance to the player,
    drawing each item in the list
    in reverse order (farthest thing first, closest thing last)
    :param surface: surface to draw things to
    :param game: cast list, do I really need this????
    :param walls: Walls previously generated with build_z_buffer
    :return: nothing
    """
    dp = distance_to_point
    for actor in game.actors:
        a = is_inside(game.player.pos,
                      get_left_fov_extreme_point(game.player),
                      get_right_fov_extreme_point(game.player),
                      actor.pos)
        b = check_viewable(game.player, actor, walls)
        # Is the actor in the player's fov and render distance with no walls obstructing it?
        if a and b:
            sx = int(actor.sprite.get_width() * (1 / dp(game.player.pos, actor.pos)))
            sy = int(actor.sprite.get_height() * (1 / dp(game.player.pos, actor.pos)))
            # Scale the sprite based on distance
            scaled = pg.transform.scale(actor.sprite, (sx, sy))
            x, y = get_actor_coords(game.player, actor)
            surface.blit(scaled, (x, y, scaled.get_width(), scaled.get_height()))


def draw_minimap(surface, game, walls):
    """
    DEBUG TOOL
    :param surface:
    :param game:
    :param walls:
    :return:
    """

    pg.draw.rect(surface, pg.Color("Black"),
                 (SCREEN_WIDTH - (LEVEL_WIDTH * LEVEL_CELL_SPACING),
                  0,
                  LEVEL_WIDTH * LEVEL_CELL_SPACING,
                  LEVEL_HEIGHT * LEVEL_CELL_SPACING))

    # Translate the current player's position to the mini map structure
    player_pos = (int(RENDER_MINI_MAP_OFFSET + (game.player.pos.x * LEVEL_CELL_SPACING)),
                  int(game.player.pos.y * LEVEL_CELL_SPACING))

    # Draw the player fov
    ra = get_right_minimap_extreme(player_pos, game.player.angle, game.player.fov, 200)
    la = get_left_minimap_extreme(player_pos, game.player.angle, game.player.fov, 200)
    pg.draw.line(surface, pg.Color("Blue"), player_pos, ra, 1)
    pg.draw.line(surface, pg.Color("Blue"), player_pos, la, 1)

    # Player
    pg.draw.circle(surface, pg.Color("red"), player_pos, 1)

    for wall in game.level.walls:
        start = (int(RENDER_MINI_MAP_OFFSET + (wall.p1.x * LEVEL_CELL_SPACING)),
                 int(wall.p1.y * LEVEL_CELL_SPACING))
        end = (int(RENDER_MINI_MAP_OFFSET + (wall.p2.x * LEVEL_CELL_SPACING)),
               int(wall.p2.y * LEVEL_CELL_SPACING))
        pg.draw.line(surface, pg.Color("Green"), start, end, 1)
    for wall in walls:
        try:
            ls = (int(RENDER_MINI_MAP_OFFSET + (wall.p1.x * LEVEL_CELL_SPACING)),
                  int(wall.p1.y * LEVEL_CELL_SPACING))
            le = (int(RENDER_MINI_MAP_OFFSET + (wall.p2.x * LEVEL_CELL_SPACING)),
                  int(wall.p2.y * LEVEL_CELL_SPACING))
            pg.draw.line(surface, pg.Color("Red"), ls, le, 1)
        except IndexError:
            logger.log("index error")
        except TypeError:
            logger.log("Type error")
    for actor in game.actors:
        pos = (int(RENDER_MINI_MAP_OFFSET + (actor.pos.x * LEVEL_CELL_SPACING)),
               int(actor.pos.y * LEVEL_CELL_SPACING))
        ra = get_right_minimap_extreme(pos, actor.angle, actor.fov, 20)
        la = get_left_minimap_extreme(pos, actor.angle, actor.fov, 20)
        pg.draw.line(surface, pg.Color("Blue"), pos, ra, 1)
        pg.draw.line(surface, pg.Color("Blue"), pos, la, 1)
        pg.draw.circle(surface, pg.Color("red"), pos, 1)


# Below are the supporting functions
# These all need error checking, type checking, and comments

def check_viewable(actor1, actor2, walls):
    """
    Answers the question "Can this actor see that actor?"
    :param actor1: Source actor
    :param actor2: Target actor
    :param walls: A list of walls to be checked
    :return: True / False
    """
    v = Line(actor1.pos, actor2.pos)
    for w in walls:
        if line_intersection(v, Line(w.p1, w.p2)):
            return False
    return True


def get_actor_coords(actor1, actor2):
    """
    Returns the x, y position of an actor passed to this function by calculating
        how far from the left fov extreme it is
    :param actor1: Source actor
    :param actor2: Target actor
    :return:
    """
    l = Line(actor1.pos, get_left_fov_extreme_point(actor1))
    r = Line(actor1.pos, get_right_fov_extreme_point(actor1))
    x = get_x_coordinate(actor1, actor2.pos, l, r)
    y = SCREEN_HEIGHT / 2
    return x, y


def get_x_coordinate(entity, point, l, r):
    """
    This is really bad and needs to get re-worked
    Measure the angle from the left and right sides at
    the distance of the point, we cant then normalise this value
    to an x coordinate on the screen
    It causes a fisheye camera, but it works and works faster
    than the previous 3 or so ideas I've had
    See readme for more info on render issues
    :param entity: Current player, camera
    :param point: Point we're evaluating
    :param l: Current player's left fov max (Line)
    :param r: Current player's right fov max (Line)
    :return: x coordinate normalised for the screen
    """
    if fuzzy_is_on_line(point, l):
        return 0
    if fuzzy_is_on_line(point, r):
        return SCREEN_WIDTH
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
    Checks if a point is ROUGHLY on a line because of floating point maths in line intersection
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
    Takes two line objects and checks if they intersect,
    if they do return the x, y coordinate of the intersection
    else return False

    Using the following resource I was able to build
    a faster implementation of this than using the
    shapely library which was far too slow for these purposes
    (This is better but possibly not the final solution)
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
    return False


def calc_ceiling(d):
    """
    Gets the ceiling height of something based on the distance
    :param d:
    :return:
    """
    return (SCREEN_HEIGHT / 2.0) - SCREEN_HEIGHT / d


def calc_floor(c):
    return SCREEN_HEIGHT - c


def point_in_view(actor, point):
    """
    Checks if a point is in an actor's vision
    :param actor: Source actor position (Entity object)
    :param point: Point we're checking (Point object)
    :return: True/False
    """
    l = get_left_fov_extreme_point(actor)
    r = get_right_fov_extreme_point(actor)
    return is_inside(actor.pos, l, r, point)


def is_inside(a, b, c, p):
    """
    Creates smaller triangles and a large triangle, if the smaller areas add up to the big area
    the point is in the big triangle
    :param a: Source actor position
    :param b: get_left_fov_extreme_point
    :param c: get_right_fov_extreme_point
    :param p: Point we're evaluating
    :return: Bool, True / False
    """
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
    # is same as abc
    r = pbc + pac + pab
    return bool(r - 0.5 <= abc <= r + 0.5)


# Standardise angles for easy maths
def get_right_fov_extreme_ang(actor):
    """
    :param actor: Actor object
    :return:
    """
    return actor.angle + actor.fov / 2


def get_left_fov_extreme_ang(actor):
    """
    :param actor: Entity object
    :return:
    """
    return actor.angle - actor.fov / 2


def get_right_fov_extreme_point(actor, d=RENDER_DEPTH):
    """
    :param actor: Entity object
    :param d: distance to offset the point
    :return: Point obj at the right extreme of the actor's FOV
    """
    return Point(actor.pos.x - d * sin(actor.angle + actor.fov / 2),
                 actor.pos.y + d * cos(actor.angle + actor.fov / 2))


def get_left_fov_extreme_point(actor, d=RENDER_DEPTH):
    """
    :param actor: Entity object
    :param d: distance to offset the point
    :return: Point obj at the left extreme of the actor FOV
    """
    return Point(actor.pos.x - d * sin(actor.angle - actor.fov / 2),
                 actor.pos.y + d * cos(actor.angle - actor.fov / 2))


def get_right_minimap_extreme(p, a, f, d=200):
    """
    DEBUGGING TOOL for the minimap, gets the endpoint for the right fov extreme
    :param p: position Point obj
    :param a: angle in radians
    :param f: FOV angle in radians
    :param d: distance to offset the point
    :return: tuple (x, y) of the right FOV extreme
    """
    return int(p[0] - d * sin(a + f / 2)), int(p[1] + d * cos(a + f / 2))


def get_left_minimap_extreme(p, a, f, d=200):
    """
    DEBUGGING TOOL for the minimap, gets the endpoint for the left fov extreme
    :param p: position Point obj
    :param a: angle in radians
    :param f: FOV angle in radians
    :param d: distance to offset the point
    :return: tuple (x, y) of the left FOV extreme
    """
    return int(p[0] - d * sin(a - f / 2)), int(p[1] + d * cos(a - f / 2))


def get_angle(actor, endpoint, point):
    """
    :param actor: actor we're measuring from
    :param endpoint: Fov arm endpoint (get_*_fov_extreme_point()) Check readme for more info
    :param point: Point we're getting the angle to
    :return: Radians
    """
    a = np.array([actor.pos.x, actor.pos.y])
    b = np.array([endpoint.x, endpoint.y])
    c = np.array([point.x, point.y])
    ba = b - a
    bc = b - c
    cos_ang = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    return np.arccos(cos_ang) * 10
