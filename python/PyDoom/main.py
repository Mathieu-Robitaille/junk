import sys

import pygame as pg
import logger

from game import Game
from globals import *
from menu import Menu
from pydoom import PyDoom


class Doom(PyDoom):
    def __init__(self):
        # Init pygame so we can use the display
        pg.init()

        # If the pygame font requirements are present instantiate the fonts
        if pg.font:
            pg.font.init()

        super().__init__()


        # Object to govern game time
        self.clock = pg.time.Clock()

        # Value with which to calculate physics
        self.frame_time = 0.0

        # Init the display
        self.surface = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # In this game each "screen" is considered something that may have differing
        # methods to handle data. ex: on the game screen W, A, S, D would move the player,
        # While the menu screen may use W and S to navigate menu options
        self.screens = [Menu("Main"), Menu("Options"), Game()]

        # Defaulting the game to start at the menu screen so we have the option to
        # load the previous game save, change options, etc...
        self.active = SCREEN_MENU

    def draw(self, surface):
        super().draw(surface)
        self.surface.fill(pg.Color("black"))
        # Draw the active screen
        self.screens[self.active].draw(surface)
        fps = "fps : {:.2f}".format(self.clock.get_fps())
        logger.on_screen_log(fps, surface)
        pg.display.update()

    def run(self):
        while True:
            self.clock.tick()
            self.frame_time = self.clock.get_time() / 1000
            super().run()
            for event in pg.event.get():
                self.event(event)
            # Update the currently active screen
            self.update(self.frame_time)
            self.draw(self.surface)

    def update(self, frame_time):
        super().update(self.frame_time)
        self.screens[self.active].update(self.frame_time)

    def event(self, event):
        if event.type == pg.QUIT:
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_1:
                self.change_to_menu()
            if event.key == pg.K_ESCAPE:
                sys.exit()
        if self.active in (SCREEN_MENU, SCREEN_OPTIONS):
            self.screens[self.active].event(event, pydoomobj=self)
        else:
            self.screens[self.active].event(event)

    def change_to_menu(self):
        self.active = SCREEN_MENU

    def change_to_options(self):
        self.active = SCREEN_OPTIONS

    def change_to_game(self):
        self.active = SCREEN_GAME


def main():
    Doom().run()


if __name__ == "__main__":
    print("PyDoom version", VERSION)
    main()
