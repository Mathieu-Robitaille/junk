import pygame as pg
from timeit import default_timer as timer
from entity import Player
from level import Level
from pydoom import PyDoom
from render_manager import draw_level


class Game(PyDoom):
    def __init__(self):
        super().__init__()
        self.level = Level()
        self.player = Player(self)

    def draw(self, surface):
        # Hand off the render responsibilities to the render manager
        start = timer()
        draw_level(self, surface)
        end = timer()
        # print(end - start)

    def update(self):
        super().update()

        # Globalupdate order should be Level, entities
        self.level.update()
        self.player.update()

    def event(self, event, timer):
        super().event(event, timer)
        self.player.event(event, timer)
