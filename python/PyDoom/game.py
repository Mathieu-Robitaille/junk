import pygame as pg
import logger
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

    def draw(self, surface, clock=None):
        # Hand off the render responsibilities to the render manager
        # start = timer()
        draw_level(self, surface)
        fps = "{:.3f}".format(clock.get_fps())
        logger.on_screen_log(fps, surface)

    def update(self):
        super().update()

        # Globalupdate order should be Level, entities
        self.level.update()
        self.player.update()

    def event(self, event, event_timer):
        super().event(event, event_timer)
        self.player.event(event, event_timer)
