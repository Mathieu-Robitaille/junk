import pygame as pg
from pydoom import PyDoom

from globals import *

GREEN = (0, 255, 0)

class Menu(PyDoom):
    def __init__(self):
        super().__init__()

    def draw(self, surface):
        pg.draw.circle(surface, GREEN,
                       (int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2)),
                       int(SCREEN_WIDTH / 3))

    def event(self, event):
        pass