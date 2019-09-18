import pygame as pg
from globals import *
from pydoom import PyDoom

class Game(PyDoom):
    def __init__(self):
        super().__init__()

    def draw(self, surface):
        pg.draw.rect(surface, (255, 255, 255),
                     (SCREEN_WIDTH / 4, SCREEN_HEIGHT / 4,
                      SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4))

    def event(self, event):
        super().event(event)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                pass
            if event.key == pg.K_a:
                pass
            if event.key == pg.K_s:
                pass
            if event.key == pg.K_d:
                pass


