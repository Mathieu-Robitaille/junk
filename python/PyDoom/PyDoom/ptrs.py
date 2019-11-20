"""
Is this a good idea? probably not...
This file exists since I'm not sure of a better way to pass
the game object all over without making it an arg for each
and every function...

This file will contain all (or just the game) "Pointers" to
important objects

Check Imports in README

Im not sure how to properly pass data from file to file
"""

from PyDoom.game import Game

#
# Game
#
GAME_OBJ = Game()


