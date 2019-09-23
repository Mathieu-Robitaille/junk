import pygame as pg

from entity import Player
from level import Level
from pydoom import PyDoom
from render_manager import draw_level


class Game(PyDoom):
    def __init__(self):
        super().__init__()
        self.level = Level()
        self.player = Player()

    def draw(self, surface):
        # Hand off the render responsibilities to the render manager
        draw_level(self, surface)

    def update(self):
        super().update()

        # Globalupdate order should be Level, entities
        self.level.update()
        self.player.update()

    def event(self, event, timer):
        super().event(event, timer)
        self.player.event(event, timer)
