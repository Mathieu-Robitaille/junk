from math import floor
from random import randint, choice
import logger
from globals import *


"""
This is a chunk of code to be used to generate random levels should
I decide to move further with that.
However, since Doom did not use random generation we'll revisit
that idea after the base game is finished as a bonus feature
"""



class Room:
    def __init__(self, room_id, cells):
        self.cells = []
        self.id = room_id
        self.global_cells = cells
        self.limX, self.limY = sizer()
        self.top_left_cell_id = room_pos()
        self.starting_cell = self.get_starting_cell()
        self.available_area = self.flood_fill()
        self.walls = set(self.cells) - self.available_area

    def get_starting_cell(self):
        """Get the first available cell starting from the top left that is not a wall"""
        for cell in self.cells:
            # Second room_id check is not necessary, however it makes the core idea
            # more transparent
            if not cell.is_wall and cell.room_id is None:
                return cell

    def get_cells(self):
        """Get the cells in the designated area for this room and assign them the room id"""
        for i in range(self.limY):
            for j in range(self.limX):
                # noinspection PyTypeChecker
                index = self.top_left_cell_id + j * i
                if self.global_cells[index].room_id is not None:
                    continue
                self.cells.append(self.global_cells[index])
                self.global_cells[index].room_id = self.id

    def flood_fill(self):
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

        # Added expanded position variables for ease of use, We're keeping self.position
        # since it allows us to use old code without rewriting it immediately (This will need
        # to be re written)
        # TODO: Remove cell.position in favor of cell.x and cell.y for clarity of code
        self.x = cell_id % self.level_width
        self.y = floor(cell_id / self.level_width)

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
    rooms = []
    for i in range(num_rooms):
        rooms.append((i, Room(i, cells)))
    # Create paths between rooms
    return cells, rooms



def sizer():
    """Returns the (x, y) size max of a room"""
    size = ROOM_SIZE + 1  # Account for off by one of range
    result = []
    # N and I are two divisors of room size, where if you multiply one with the other
    # You'll end with ROOM_SIZE
    for i in range(1, size):
        n = size / i if size / i % 1 == 0 else 0
        if i < 3 or n < 3:
            continue
        if size % i == 0:
            result.append((i, n))
    return choice(result)

def room_pos():
    return randint(1, LEVEL_WIDTH), randint(1, LEVEL_HEIGHT)


def dist_to(a, b):
    """
    Get the distance from one position to another
    Main usage is figuring out if rooms are too close
    """
    r = (abs(a[0] - b[0]), abs(a[1] - b[1]))


class Level():
    def __init__(self):
        super().__init__()
        # Width, Height
        self.width = LEVEL_WIDTH
        self.height = LEVEL_HEIGHT
        self.map, self.rooms = create_world(self.width, self.height)

    def update(self):
        pass
