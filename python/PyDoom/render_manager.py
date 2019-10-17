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
    # localise these vars as it's more clear plus python accesses local variables faster
    # Expand player position for clarity
    player_pos_x = game.player.pos[0]
    player_pos_y = game.player.pos[1]
    player_angle = game.player.angle
    player_fov = game.player.fov

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
            if game.level.map[int(test_y * game.level.width + test_x)].is_wall:
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

    draw_screen(surface, cast_list)
    draw_minimap(surface, game)


def draw_screen(surface, casts):
    # Draw each cast as a vertical line to be matched up with the next cast for
    # smoooooth walls
    for i in range(len(casts)):
        try:
            if i + 1 >= len(casts):
                continue

            if casts[i][0] is 0 and casts[i][1] is 0:
                continue  # I'm super good at coding

            # The X offsets of the current vertical line and the subsequent line
            x1 = casts[i][2]
            x2 = casts[i][2]
            val = casts[i][3]
            color = (val, val, val)

            coordinates = [(x1, casts[i][0]),  # Ceiling of current cell
                           (x1, casts[i + 1][0]),  # Ceiling of next cell
                           (x2, casts[i][1]),  # Floor of current cell
                           (x2, casts[i + 1][1])]  # Floor of next cell
            pg.draw.polygon(surface, color, coordinates, 0)
        except IndexError as e:  # e here incase I want to use it later,
            print("you done it now boy")


def draw_minimap(surface, game):
    for h in range(0, LEVEL_HEIGHT):
        for w in range(0, LEVEL_WIDTH):
            if game.level.map[(LEVEL_WIDTH*h) + w].is_wall:
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
    # Change variable name, its bad
    # Subtract 1.54 to correct for angle issues
    player_aim_line_end = (player_pos[0] + 5 * sin(game.player.angle),
                           player_pos[1] + 5 * cos(game.player.angle))
    pg.draw.line(surface, pg.Color("white"), player_pos, player_aim_line_end)


def shadow_cast(game):
    pass  # Same as edge detection

