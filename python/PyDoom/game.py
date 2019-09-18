import pygame as pg
from globals import *
from pydoom import PyDoom
from level import Level
from entity import Player


class Game(PyDoom):
    def __init__(self):
        super().__init__()
        self.current_level = Level()
        self.player = Player()

    def draw(self, surface):
        # NOT THE WAY TO GO, THIS SHOULD BE A CALL TO THE RENDER MANAGER
        self.current_level.draw(surface)

    def event(self, event):
        super().event(event)
        if event.type == pg.KEYDOWN:
            if event.key in (pg.K_w, pg.K_a, pg.K_s, pg.K_d):
                self.player.event(event.key)



