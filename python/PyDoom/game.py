import pygame as pg
import logger
from timeit import default_timer as timer
from entity import Player, Enemy
from level import Level
from pydoom import PyDoom
from globals import Point
from render_manager import draw


class Game(PyDoom):
    def __init__(self):
        super().__init__()
        self.level = Level()
        self.player = Player(self)
        # Temporary var for testing, I'll build a more long term solution to access actors when
        self.actors = [Enemy(self, pos=Point(x, y), sprite="imp.png") for x, y in [
            (5, 4), (13, 13), (6, 1.5), (6, 8)]]

    def draw(self, surface):
        # Hand off the render responsibilities to the render manager
        # start = timer()
        draw(self, surface)

    def update(self, frame_time):
        super().update(frame_time)

        # Update order should be actors then level because the actors change the level (doors, etc...)
        for actor in [self.player, *self.actors]:
            actor.update(frame_time)
        self.level.update(frame_time)

    def event(self, event):
        super().event(event)
        self.player.event(event)
