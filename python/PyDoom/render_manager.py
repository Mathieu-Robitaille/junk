from math import cos, sin, pi, fabs

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


def draw_level(game, surface):
    # localise these vars as its better practice and python accesses local variables faster
    # Expanded for clarity
    player_pos_x = game.player.pos[0]
    player_pos_y = game.player.pos[1]
    player_angle = game.player.angle
    player_fov = game.player.fov

    cast_list = []

    for i in range(int(SCREEN_WIDTH / RENDER_SCREEN_RAYSPLIT)):
        # Get the angle we want to cast to
        ray_angle = (player_angle - player_fov / 2.0) + float(i) / float(SCREEN_WIDTH) * player_fov

        # float to hold the distance to the wall we're raycasting towards
        distance_to_wall = 1.0

        # Check if we hit a wall, if we did this is the flag to break the while loop
        hitwall = False

        # Get the direction vector the player is looking in
        look_x = sin(ray_angle)
        look_y = cos(ray_angle)

        while not hitwall and distance_to_wall < RENDER_RAYCASTING_DEPTH:
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
            if game.level.map[int(test_y * game.level.width + test_x)] == "#":
                # We just hit a wall, set the appropriate flag
                hitwall = True
        
        # Set default values to draw infinite distance later of, however I decide to do that
        ceiling = 0
        floor = 0
        val = 0
        if hitwall:
            # Calculate the top of the walls based off the screen
            ceiling = (SCREEN_HEIGHT / 2.0) - SCREEN_HEIGHT / distance_to_wall
            # Calc the floor
            floor = SCREEN_HEIGHT - ceiling

            # Force the color value in between 0-255
            val = (255 / distance_to_wall if 255 / distance_to_wall > 0 else 0) % 255
        cast_list.append([ceiling, floor, i, val])
    for i in range(len(cast_list)):
        try:
            if i + 1 > len(cast_list):
                continue
            if cast_list[i][0] is 0 and cast_list[i][1] is 0:
                continue  # I'm super good at coding
            # This is very ugly and I'm ashamed of it, BUT it's very readable so there's that...
            x1 = cast_list[i][2]
            x2 = cast_list[i][2]
            val = cast_list[i][3]
            color = (val, val, val)
            
            coordinates = [(x1, cast_list[i][0]),  # Ceiling of current cell
                           (x1, cast_list[i+1][0]),  # Ceiling of next cell
                           (x2, cast_list[i][1]),  # Floor of current cell
                           (x2, cast_list[i+1][1])]  # Floor of next cell
            pg.draw.polygon(surface, color, coordinates, 0)
        except IndexError as e:
            print("you done it now boy")
    draw_minimap(game, surface)


def draw_minimap(game, surface):
    for h in range(0, LEVEL_HEIGHT):
        for w in range(0, LEVEL_WIDTH):
            if game.level.map[(LEVEL_WIDTH*h) + w] == "#":
                pg.draw.rect(surface, pg.Color("white"),
                             (SCREEN_WIDTH - 200 + (w * LEVEL_CELL_SPACING),
                              h * LEVEL_CELL_SPACING,
                              LEVEL_CELL_SPACING,
                              LEVEL_CELL_SPACING))
            else:
                pg.draw.rect(surface, pg.Color("black"),
                             (SCREEN_WIDTH - 200 + (w * LEVEL_CELL_SPACING),
                              h * LEVEL_CELL_SPACING,
                              LEVEL_CELL_SPACING,
                              LEVEL_CELL_SPACING))
    player_pos = (int(SCREEN_WIDTH - 200 + (game.player.pos[0] * LEVEL_CELL_SPACING)),
                 int(game.player.pos[1] * LEVEL_CELL_SPACING))
    pg.draw.circle(surface, pg.Color("red"), player_pos, 1)


def edge_detection(game):
    pass  # Nope, not using edge detection unless I implement a cell based map generation


def shadow_cast(game):
    pass  # Same as edge detection

