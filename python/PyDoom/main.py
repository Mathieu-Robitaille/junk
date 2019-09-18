from globals import *
from pydoom import PyDoom
from game import Game
from menu import Menu

import pygame as pg
import game
import menu
import sys


class Doom(PyDoom):
    def __init__(self):
        pg.init()

        # If the pygame font requirements are present instantiate the fonts
        if pg.font:
            pg.font.init()

        super().__init__()

        # Init the display
        self.surface = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # In this game each "screen" is considered something that may have differing
        # methods to handle data. ex: on the game screen W, A, S, D would move the player,
        # While the menu screen may use W and S to navigate menu options
        self.screens = [Menu(), Game()]

        # Defaulting the game to start at the menu screen so we have the option to
        # load the previous game save, change options, etc...
        self.active = SCREEN_MENU



    def draw(self, surface):
        super().draw(surface)
        self.surface.fill(pg.Color("black"))
        # Draw the active screen
        self.screens[self.active].draw(surface)
        pg.display.update()

    def run(self):
        while True:
            super().run()
            for event in pg.event.get():
                self.event(event)
            # Update the currently active screen
            self.update()
            self.draw(self.surface)

    def update(self):
        super().update()
        self.screens[self.active].update()

    def event(self, event):
        if event.type == pg.QUIT:
            # We may want to change this to a method giving the player an option to say no
            # in the event this was selected by accident
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.change_to_game()
            if event.key == pg.K_1:
                self.change_to_menu()
        # THIS NEEDS TO CHANGE, RIGHT NOW IT WILL ALLOW
        # THE USER TO CHANGE BACK AND FORTH BETWEEN SCREENS
        # JUST BY PLAYING THE GAME
        self.screens[self.active].event(event)


    def change_to_menu(self):
        self.active = SCREEN_MENU

    def change_to_game(self):
        self.active = SCREEN_GAME


def main():
    Doom().run()


if __name__ == "__main__":
    print("PyDoom version", VERSION)
    main()