from math import floor
from random import randint, choice
import logger
from globals import *

class Room:
    def __init__(self, room_id, top_left_cell_id):
        self.top_left_cell_id = top_left_cell_id
        self.id = room_id
        self.limX, self.limY = sizer()
        self.cells = []
        self.starting_cell = self.getstarting_cell()
        self.available_area = self.floodfill()
        self.walls = set(self.cells) - self.available_area

    def getstarting_cell(self):
        for cell in self.cells:
            if not cell.is_wall:
                return cell

    def floodfill(self):
        contenders = [self.starting_cell]
        result = [self.starting_cell]
        while len(contenders) > 0:
            cell = contenders.pop()
            try:
                if cell.visited or cell.is_wall:
                    continue
                cell.visited = True
                if cell.id - self.limX >= 0:
                    if not self.cells[cell.id - self.limX].is_wall:
                        contenders.append(self.cells[cell.id - self.limX])
                        result.append(self.cells[cell.id - self.limX])
                if cell.id + self.limX < ROOM_SIZE:
                    if not self.cells[cell.id + self.limX].is_wall:
                        contenders.append(self.cells[cell.id + self.limX])
                        result.append(self.cells[cell.id + self.limX])
                if (cell.id % self.limX) + 1 < self.limX:
                    if not self.cells[cell.id + 1].is_wall:
                        contenders.append(self.cells[cell.id + 1])
                        result.append(self.cells[cell.id + 1])
                if (cell.id % self.limX) - 1 > 0:
                    if not self.cells[cell.id - 1].is_wall:
                        contenders.append(self.cells[cell.id - 1])
                        result.append(self.cells[cell.id - 1])
            except IndexError:
                logger.log("Out of range error, cell_id : {}".format(cell.id))
        return set(result)


class Cell:
    def __init__(self, cell_id, level_width, level_height):
        self.id = cell_id
        self.level_width = level_width
        self.level_height = level_height

        # [0] = x, [1] = y
        self.position = (cell_id % self.level_width, floor(cell_id / self.level_width))
        # Added expanded position variables for ease of use, We're keeping self.position
        # since it allows us to use old code without rewriting it immediately (This will need
        # to be re written)
        # TODO: Remove cell.position in favor of cell.x and cell.y for clarity of code
        self.x = self.position[0]
        self.y = self.position[1]

        # The ID of the edge assigned to this cell for each cardinal direction
        # order is always north, south, east, west
        self.edge_id = [0, 0, 0, 0]

        # Edges in order of North, South, East, and West
        self.edges = [False, False, False, False]

        # Is this a path between two rooms?
        self.is_path = False

        # Is this a part of the level geometry the player can explore
        self.is_wall = False

        # is this cell part of a room
        self.is_room = False

        # Has room generation visited this cell?
        self.visited = False

        # Which room is this cell a part of?
        self.room_id = 0


def create_world(w, h):
    cells = [Cell(i, w, h) for i in range(LEVEL_SIZE)]
    num_rooms = randint(ROOM_COUNT_MIN, ROOM_COUNT_MAX)
    for i in range(num_rooms):
        x, y = randint(1, w), randint(1, h)


def sizer():
    # Returns the (x, y) size max of a room
    size = ROOM_SIZE + 1
    result = []
    for i in range(1, size):
        n = size / i if size / i % 1 == 0 else None
        if i < 3 or n < 3:
            continue
        if (size % i == 0) and n is not None:
            result.append((i, n))
    return choice(result)

def dist_to(a, b):
    r = (abs(a[0] - b[0]), abs(a[1] - b[1]))


class Level():
    def __init__(self):
        super().__init__()
        # Width, Height
        self.width = LEVEL_WIDTH
        self.height = LEVEL_HEIGHT
        self.map = create_world(self.width, self.height)

    def update(self):
        pass
