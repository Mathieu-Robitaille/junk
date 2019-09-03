#!/usr/bin/env python

# Author: Mathieu Robitaille

# Possible optimisations :
# Use A* cells on initial world generation if A* is the search algo being used
# TODO: Add node based pathing, ex: a long corridor with no branches could have each end be neighbors of each other

import sys
import pygame

from search import StarSearch, FloodFill
from world import World
# I'm pretty sure wildcard imports are bad?
from mazeglobals import *


class PyGameObj(object):
    def __init__(self, random_paths, verbose):
        # Set up the core object used to draw to the screen and hold the maze data
        pygame.init()
        pygame.display.set_caption("Mathieu Robitaille's Maze Generation")
        self.screen = pygame.display.set_mode(
            (MAZE_WIDTH * (WALL_WIDTH + PATH_WIDTH),
             MAZE_HEIGHT * (WALL_WIDTH + PATH_WIDTH)))
        self.w = World()
        self.stack = [self.w.cells[0]]
        self.search_type = 0
        self.searches = []
        self.solved = False
        self.verbose = verbose
        self.random_paths = (random_paths, False)

    def run(self):
        # This holds the main while loop for the maze generation and the control logic for which
        # search algorithm will solve the maze
        while True:
            self.event_loop()
            if len(self.stack) == 0:
                self.search_picker()
            if self.verbose or len(self.searches) is not 0:
                self.draw()
                if len(self.searches) is not 0:
                    self.searches[self.search_type].draw()
            # Place update call here as update may have some specific
            # draw calls to make we do not want over write
            self.update()
            pygame.display.update()

    def event_loop(self):
        # Check if the user is trying to exit the pygame instance
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
                    sys.exit()
                elif event.key == pygame.K_UP and self.search_type < len(self.searches) - 1:
                    self.search_type += 1
                    print("Increasing search type to : " + str(self.search_type))
                elif event.key == pygame.K_DOWN and self.search_type > 0:
                    self.search_type -= 1
                    print("Decreasing search type to : " + str(self.search_type))

    def draw(self):
        # Fairly bloated draw cycle.
        # This can get cut down I'm certain
        # TODO: This should probably be in the world class as this is drawing the world
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
        if len(self.searches) is not 0:
            return
        # Only one pathing algo right now
        if self.random_paths[0]:
            self.random_paths = (not self.random_paths[0], self.w.random_paths())
        self.searches.append(StarSearch(self.w, self.screen))
        self.searches.append(FloodFill(self.w, self.screen))

    def update(self):
        # Very simple update cycle as of now.
        # This is where it would make sense to put pathing algo updates
        # with algos like flood fill or breadth/depth first allowing us to
        # see the path being built
        if len(self.stack) > 0:
            self.w.update(self.stack)
        else:
            for search in self.searches:
                search.update()


def make_maze():
    # TODO: Proper input handling
    # search_type = input("\nAvailable search types are : \n\n\t1) A* Search\n\t2) Flood fill\n\t"
    #                     "Please make your selection by entering a number -> ")
    PyGameObj(random_paths=True, verbose=True).run()


if __name__ == "__main__":
    make_maze()
    input()
