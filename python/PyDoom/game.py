import pygame as pg
from globals import *
from pydoom import PyDoom
from level import Level
from entity import Player
from render_manager import draw_level


class Game(PyDoom):
    def __init__(self):
        super().__init__()
        self.level = Level()
        self.player = Player()

    def draw(self, surface):
        # Hand off the render responsibilities to the render manager
        draw_level(self, surface)

    def event(self, event):
        super().event(event)
        if event.type == pg.KEYDOWN:
            if event.key in (pg.K_w, pg.K_a, pg.K_s, pg.K_d):
                self.player.event(event.key)



