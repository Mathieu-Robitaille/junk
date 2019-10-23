from math import cos, sin, pi, fabs, sqrt

import pygame as pg

from globals import *

edges = []


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


def draw_level(g, s):
    # localise these vars as it's more clear plus python accesses local variables faster
    # Expand player position for clarity
    player_pos_x = g.player.pos[0]
    player_pos_y = g.player.pos[1]
    player_angle = g.player.angle
    player_fov = g.player.fov

    cast_list = []

    for i in range(int(SCREEN_WIDTH)):
        # Get the angle we want to cast to
        ray_angle = (player_angle - player_fov / 2.0) + float(i) / float(SCREEN_WIDTH) * player_fov

        # float to hold the distance to the wall we're raycasting towards
        distance_to_wall = 1.0

        # Check if we hit a wall, if we did this is the flag to break the while loop
        hit_wall = False

        # Get the direction vector the player is looking in
        look_x = sin(ray_angle)
        look_y = cos(ray_angle)

        while not hit_wall and distance_to_wall < RENDER_RAYCASTING_DEPTH:
            # TODO: dist here causes blocky walls, what can I do to fix this?
            # Right now this is fairly efficient in terms of getting the rough idea on the screen
            # But it's not very pretty
            #
            # Another idea would be to smooth lines over a larger area, example would be
            # Look 20 steps ahead, if the value is +/- 1 dist then calc a slope for the next 20 steps???
            # Or I could find a better method of finding the exact distance to the wall, this would
            # also solve the problem but may be too resource heavy for python,,,

            # another idea would be to use edgefinding on all walls, casting to visible walls,
            # calculating the exact distance to each "vertical edge" or corner
            # then calculating the slope between each corner

            distance_to_wall += 0.1

            test_x = int(player_pos_x + look_x * distance_to_wall)
            test_y = int(player_pos_y + look_y * distance_to_wall)

            # This needs to change
            if g.level.map[two_d_to_one_d((test_x, test_y), g.level.width)].is_wall:
                # We just hit a wall, set the appropriate flag
                hit_wall = True
        
        # Set default values to draw infinite distance later of, however I decide to do that
        ceiling = 0
        floor = 0
        val = 0

        if hit_wall:

            # Calculate the top of the walls based off the screen
            ceiling = (SCREEN_HEIGHT / 2.0) - SCREEN_HEIGHT / distance_to_wall

            # Calc the floor
            floor = SCREEN_HEIGHT - ceiling

            # Force the color value in between 0-255
            val = (255 / distance_to_wall if 255 / distance_to_wall > 0 else 0) % 255

        cast_list.append([ceiling, floor, i, val])

    draw_screen(s, cast_list)
    draw_sprites(s, cast_list)
    draw_minimap(s, g)


def draw_screen(s, c):
    # Draw each cast as a vertical line to be matched up with the next cast for
    # smoooooth walls

    # Draw the sky
    pg.draw.rect(s, (135, 206, 235),
                 (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT / 2))

    # Draw the floor so its prettier
    pg.draw.rect(s, (0, 64, 0),
                 (0, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT / 2))

    for i in range(len(c)):
        try:
            if i + 1 >= len(c):
                continue  # finish the wall

            if c[i][0] is 0 and c[i][1] is 0:
                continue  # I'm super good at coding

            # The X offsets of the current vertical line and the subsequent line
            x1 = c[i][2]
            x2 = c[i + 1][2]
            val = c[i][3]
            color = (val, val, val)

            coordinates = [(x1, c[i][0]),  # Ceiling of current cell
                           (x1, c[i + 1][0]),  # Ceiling of next cell
                           (x2, c[i][1]),  # Floor of current cell
                           (x2, c[i + 1][1])]  # Floor of next cell
            pg.draw.polygon(s, color, coordinates, 0)
        except IndexError as e:  # e here incase I want to use it later,
            print("you done it now boy")


def draw_sprites(s, c):
    pass


def draw_minimap(s, g):
    for h in range(0, LEVEL_HEIGHT):
        for w in range(0, LEVEL_WIDTH):
            if g.level.map[two_d_to_one_d((w, h), g.level.width)].is_wall:
                pg.draw.rect(s, pg.Color("white"),
                             (SCREEN_WIDTH - LEVEL_CELL_SPACING - (w * LEVEL_CELL_SPACING),
                              h * LEVEL_CELL_SPACING,
                              LEVEL_CELL_SPACING,
                              LEVEL_CELL_SPACING))
            else:
                pg.draw.rect(s, pg.Color("black"),
                             (SCREEN_WIDTH - LEVEL_CELL_SPACING - (w * LEVEL_CELL_SPACING),
                              h * LEVEL_CELL_SPACING,
                              LEVEL_CELL_SPACING,
                              LEVEL_CELL_SPACING))

    player_pos = (int(SCREEN_WIDTH - (g.player.pos[0] * LEVEL_CELL_SPACING)),
                  int(g.player.pos[1] * LEVEL_CELL_SPACING))

    # Change variable name, very bad
    player_aim_line_end = (player_pos[0] - 7 * sin(g.player.angle),
                           player_pos[1] + 7 * cos(g.player.angle))

    # Player aim line
    pg.draw.line(s, pg.Color("white"), player_pos, player_aim_line_end)

    # Player
    pg.draw.circle(s, pg.Color("red"), player_pos, 1)


"""
I now have a way to calculate the exact distance between two points and where two lines intersect.
Now what i need to work on is creating the lines representing the walls, then use linear to figure out which
walls i can see, THEN calculate the exact distance to those walls.
All of this to make the walls less jagged...
"""


def line_intersection(l1, l2):
    """

    :param l1: The start and end points of a line ex: ((x1, y1), (x2, y2))
    :param l2: The start and end points of a line to be checked in the same format as param 1
    :return: The intersection point of those lines, if they don't, return (-1, -1)
    """
    xdiff = (l1[0][0] - l1[1][0], l2[0][0] - l2[1][0])
    ydiff = (l1[0][1] - l1[1][1], l2[0][1] - l2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        return -1, -1

    d = (det(*l1), det(*l2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


def distance_to_point(a, b):
    """
    A simple point to point distance measure tool
    :param a: x, y coords of point a
    :param b: x, y coords of point a
    :return: float: distance between a and b
    """
    return sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)



