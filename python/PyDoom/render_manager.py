from math import cos, sin, pi
import pygame as pg
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


def draw_level(game, surface):
    pass


def draw_minimap(game, surface):
    for i in game.level.map:
        pg.draw.rect(surface, pg.Color("white"),
                     (i.position[0] * CELL_SPACING + PATH_OFFSET,
                      i.position[1] * CELL_SPACING + PATH_OFFSET,
                      CELL_SPACING / 2,
                      CELL_SPACING / 2))
        if i.path[0]:
            pg.draw.rect(surface, pg.Color("white"),
                         (i.position[0] * CELL_SPACING + PATH_OFFSET + (CELL_SPACING / 8),
                          i.position[1] * CELL_SPACING + PATH_OFFSET,
                          CELL_SPACING / 4,
                          CELL_SPACING))
        if i.path[1]:
            pg.draw.rect(surface, pg.Color("white"),
                         (i.position[0] * CELL_SPACING + PATH_OFFSET,
                          i.position[1] * CELL_SPACING + PATH_OFFSET + (CELL_SPACING / 8),
                          CELL_SPACING,
                          CELL_SPACING / 4))
