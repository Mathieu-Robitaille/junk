import pygame as pg
import logger
from timeit import default_timer as timer
from entity import Player
from level import Level
from pydoom import PyDoom
from render_manager import draw


class Game(PyDoom):
    def __init__(self):
        super().__init__()
        self.level = Level()
        self.player = Player(self)

    def draw(self, surface):
        # Hand off the render responsibilities to the render manager
        # start = timer()
        draw(self, surface)

    def update(self, frame_time):
        super().update(frame_time)

        # Globalupdate order should be Level, entities
        self.level.update(frame_time)
        self.player.update(frame_time)

    def event(self, event):
        super().event(event)
        self.player.event(event)
