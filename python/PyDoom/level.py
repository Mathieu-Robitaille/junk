from math import floor
from random import randint, choice
import logger
from globals import *


def create_world(width, height):
    # Return default test value
    return "###############" \
           "#             #" \
           "#             #" \
           "#             #" \
           "#             #" \
           "#   #     #   #" \
           "#   #     #   #" \
           "#   #     #   #" \
           "#   #     #   #" \
           "#   #  #  #   #" \
           "#             #" \
           "#             #" \
           "#             #" \
           "#             #" \
           "###############"


class Level:
    def __init__(self):
        super().__init__()
        # Width, Height
        self.width = LEVEL_WIDTH
        self.height = LEVEL_HEIGHT
        self.map = create_world(self.width, self.height)

    def update(self):
        pass
