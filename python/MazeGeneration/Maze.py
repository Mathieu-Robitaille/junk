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


# Declare global vars, some of these may be better suited being placed elsewhere
# ex: the width vars could be set as defaults for make maze, then use sys.args
# to populate the vars from command line if we want something different

WALL_WIDTH = 2 * 4
PATH_WIDTH = 4 * 4
MAZE_WIDTH = 64
MAZE_HEIGHT = 32
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)


class PyGameObj(object):
    def __init__(self, search_type):
        # Set up the core object used to draw to the screen and hold the maze data
        self.screen = pygame.display.set_mode(
            (MAZE_WIDTH * (WALL_WIDTH + PATH_WIDTH),
             MAZE_HEIGHT * (WALL_WIDTH + PATH_WIDTH)))
        pygame.init()
        pygame.display.set_caption("Cunning-Journeyman's Maze Generation")
        self.w = World(MAZE_WIDTH, MAZE_HEIGHT, WALL_WIDTH, PATH_WIDTH)
        self.stack = [self.w.cells[0]]
        self.search_type = search_type
        self.solved = False
        self.path = []

    def run(self, verbose):
        # This holds the main while loop for the maze generation and the control logic for which
        # search algorithm will solve the maze
        while True:
            self.event_loop()
            if len(self.stack) > 0:
                self.update()
            else:
                self.search_picker()
                time.sleep(1)
                self.draw()
                pygame.display.update()
                return
            if verbose:
                self.draw()
                pygame.display.update()

    def event_loop(self):
        # Check if the user is trying to exit the pygame instance
        for event in pygame.event.get():
            if event.type() == pygame.QUIT:
                sys.exit()

    def draw(self):
        # Fairly bloated draw cycle.
        # This can get cut down I'm certain
        #
        # Iterated over each cell and draws it accordingly, if the search algo is done
        # draw the path
        # Right now it is only structured to work with A* searching which is either done or not.
        # Once another search algo is implemented this will need to be changed to allow a
        # fraame by frame drawing of the current path
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
        if self.solved:
            cell = self.path[-1]
            divisions = 255 / len(self.path)
            color = RED
            while cell is not self.path[0]:
                color = (color[0] - divisions if color[0] - divisions > 0 else 0, 0,
                         color[2] + divisions if color[2] + divisions < 255 else 255)
                pygame.draw.line(self.screen, color,
                                 (cell.draw_position[0] + PATH_WIDTH / 2 + 3,
                                  cell.draw_position[1] + PATH_WIDTH / 2 + 3),
                                 (cell.parent.draw_position[0] + PATH_WIDTH / 2 + 3,
                                  cell.parent.draw_position[1] + PATH_WIDTH / 2 + 3),
                                 floor(WALL_WIDTH / 2))
                cell = cell.parent

    def search_picker(self):
        # Only one pathing algo right now
        if self.search_type == "Star":
            self.solved, self.path = StarSearch(self.w).solve()

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
