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
    playerposx = game.player.pos[0]
    playerposy = game.player.pos[1]
    playerangle = game.player.angle
    playerfov = game.player.fov

    for i in range(int(SCREEN_WIDTH / SCREEN_RAYSPLIT)):
        # Get the angle we want to cast to
        rayangle = (playerangle - playerfov / 2.0) + float(i) / float(SCREEN_WIDTH) * playerfov

        # float to hold the distance to the wall we're raycasting towards
        distancetowall = 0.0

        # Check if we hit a wall, if we did this is the flag to break the while loop
        hitwall = False

        # Get the direction vector the player is looking in
        lookx = sin(rayangle)
        looky = cos(rayangle)

        while not hitwall and distancetowall < RAYCASTING_DEPTH:
            distancetowall += 0.1

            # TIME TO FIGURE OUT HOW TO DO INSIDE WALLS
            # TODO: Change render engine to use edge finding and cast to those edges

            testx = int(playerposx + lookx * distancetowall)
            testy = int(playerposy + looky * distancetowall)

            # This needs to change
            if game.level.map[int(testy * game.level.width + testx)] == "#":
                # We just hit a wall, set the appropriate flag
                hitwall = True
        if hitwall:
            # Calculate the top of the walls based off the screen
            ceiling = (SCREEN_HEIGHT / 2.0) - SCREEN_HEIGHT / distancetowall
            # Calc the floor
            floor = SCREEN_HEIGHT - ceiling

            # Force the value inbetween 0-255
            val = (255 / distancetowall if 255 / distancetowall > 0 else 0) % 255
            # CHANGE COLOR TO A TEXTURE BLIT
            color = (val, val, val)
            pg.draw.rect(surface, color,
                         (i, ceiling, SCREEN_RAYSPLIT, floor - ceiling))
        else:
            pg.draw.rect(surface, pg.Color("green"),
                         (i, SCREEN_HEIGHT / 4, SCREEN_RAYSPLIT, SCREEN_HEIGHT /2))

    #draw_minimap(game, surface)


def draw_minimap(game, surface):
    for i in game.level.map:
        x = MINI_MAP_OFFSET + (i.position[0] * CELL_SPACING + PATH_OFFSET)
        y = i.position[1] * CELL_SPACING + PATH_OFFSET
        pg.draw.rect(surface, pg.Color("white"),
                     (x, y,
                      CELL_SPACING / 2, CELL_SPACING / 2))
        if i.path[0]:
            pg.draw.rect(surface, pg.Color("white"),
                         (x + (CELL_SPACING / 8), y,
                          CELL_SPACING / 4, CELL_SPACING))
        if i.path[1]:
            pg.draw.rect(surface, pg.Color("white"),
                         (x, y + (CELL_SPACING / 8),
                          CELL_SPACING, CELL_SPACING / 4))

    # Draw player pos on map
    try:
        x = MINI_MAP_OFFSET + (game.player.pos[0] * CELL_SPACING + PATH_OFFSET)
        y = game.player.pos[1] * CELL_SPACING + PATH_OFFSET
        pg.draw.rect(surface, pg.Color("red"),
                     (x, y,
                      CELL_SPACING / 2, CELL_SPACING / 2))
    except Exception as e:
        print(e)

def edge_detection(game):
    for cell in game.level.map:
        pass