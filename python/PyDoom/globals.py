VERSION = "0.0.2"

#
# All constants must begin with const type then constname
# EX: RENDER_ for constants used by the render manager
#


#
# Pygame init constants
#
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

#
# World generation constants
#
NORTH = 0
SOUTH = 1
EAST = 2
WEST = 3
LEVEL_WIDTH = 15
LEVEL_HEIGHT = 15
LEVEL_SIZE = LEVEL_WIDTH * LEVEL_WIDTH
LEVEL_PATH_LENGTH_MIN = 3   # Random number, may need some tuning
LEVEL_PATH_LENGTH_MAX = 10  # Random number, may need some tuning
LEVEL_PATH_CHANCE = 100
LEVEL_PATH_DIRECTION_CHANCE = 50
LEVEL_CELL_SPACING = 10
LEVEL_PATH_OFFSET = 10

#
# Room size and shape logic consts
#
# The average size of rooms by way on number of cells in the room
ROOM_SIZE = 60
ROOM_CHANCE = 0.6

ROOM_COUNT_MAX = 10  # int(LEVEL_SIZE / (ROOM_SIZE / 3) / ROOM_CHANCE) + 1
ROOM_COUNT_MIN = 5   # int(ROOM_COUNT_MAX / 1.5)




#
# Render constants
#
RENDER_RAYCASTING_DEPTH = 30
# This is the divisor for ray casting, a larger number means more deg between rays
RENDER_MINI_MAP_OFFSET = SCREEN_WIDTH - (LEVEL_WIDTH * LEVEL_PATH_OFFSET) - 30

#
# Screen type "enums"
#
SCREEN_MENU = 0
SCREEN_GAME = 1

#
# Entity "enums"
#
TEAM_GAEA = 0
TEAM_PLAYER = 1
TEAM_ENEMY = 2

#
# Image utility globals
#
IU_ASSET_DIR = "assets"


#
# Logging constants
#
LOGGING_DIR = "logs"


#
#
#