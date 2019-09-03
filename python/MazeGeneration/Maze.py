#!/usr/bin/env python

# Author: Mathieu Robitaille

# Possible optimisations :
# Use A* cells on initial world generation if A* is the search algo being used


import sys
import time
from math import floor

import pygame

from search import StarSearch
from world import World
# I'm pretty sure wildcard imports are bad?
from mazeglobals import *


# Declare global vars, some of these may be better suited being placed elsewhere
# ex: the width vars could be set as defaults for make maze, then use sys.args
# to populate the vars from command line if we want something different


class PyGameObj(object):
    def __init__(self, search_type):
        # Set up the core object used to draw to the screen and hold the maze data
        pygame.init()
        pygame.display.set_caption("Cunning-Journeyman's Maze Generation")
        self.screen = pygame.display.set_mode(
            (MAZE_WIDTH * (WALL_WIDTH + PATH_WIDTH),
             MAZE_HEIGHT * (WALL_WIDTH + PATH_WIDTH)))
        self.w = World()
        self.stack = [self.w.cells[0]]
        self.search_type = search_type
        self.search = None

    def run(self, verbose):
        # This holds the main while loop for the maze generation and the control logic for which
        # search algorithm will solve the maze
        while True:
            self.event_loop()
            if len(self.stack) > 0:
                self.update()
            else:
                self.search_picker()
                self.draw()
                self.search.draw()
                pygame.display.update()
                return
            if verbose:
                self.draw()
                pygame.display.update()

    def event_loop(self):
        # Check if the user is trying to exit the pygame instance
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def draw(self):
        # Fairly bloated draw cycle.
        # This can get cut down I'm certain

        self.screen.fill(pygame.Color("black"))

        # Draw the maze as it is being built or the finished maze
        for cell in self.w.cells:
            color = BLACK
            if cell.visited:
                if cell.is_start:
                    color = BLUE
                elif cell.is_end:
                    color = RED
                else:
                    color = WHITE
            if cell.path[0]:
                pygame.draw.rect(self.screen, WHITE,
                                 (cell.draw_position[0] + (PATH_WIDTH / 4),
                                  cell.draw_position[1] + (PATH_WIDTH / 4),
                                  PATH_WIDTH * 2, PATH_WIDTH / 2))
            if cell.path[1]:
                pygame.draw.rect(self.screen, WHITE,
                                 (cell.draw_position[0] + (PATH_WIDTH / 4),
                                  cell.draw_position[1] + (PATH_WIDTH / 4),
                                  PATH_WIDTH / 2, PATH_WIDTH * 2))
            pygame.draw.rect(self.screen, color,
                             (cell.draw_position[0], cell.draw_position[1],
                              PATH_WIDTH, PATH_WIDTH))

        # Draw the head node of the stack
        if len(self.stack) > 0:
            pygame.draw.rect(self.screen, BLUE,
                             (self.stack[-1].draw_position[0], self.stack[-1].draw_position[1],
                              PATH_WIDTH, PATH_WIDTH))
        # If the maze is solved, draw the path from start to end
        # The search algo should draw its own solution

    def search_picker(self):
        # Only one pathing algo right now
        if self.search_type == "Star":
            self.search = StarSearch(self.w, self.screen)
            self.search.solve()

    def update(self):
        # Very simple update cycle as of now.
        # This is where it would make sense to put pathing algo updates
        # with algos like flood fill or breadth/depth first allowing us to
        # see the path being built
        self.w.update(self.stack)


def make_maze():
    PyGameObj("Star").run(True)


if __name__ == "__main__":
    make_maze()
    input()
