import heapq

from world import Cell as WorldCell


class Cell(WorldCell):
    def __init__(self, c, w):
        # Override the world cells as we require additional data
        # other algos will not need
        #
        # g = cost to move from the starting cell to this cell
        # h = estimation of the cost to move from this cell to end cell
        # f = g + h
        super().__init__(c.id, w.maze_width)
        self.path = c.path
        self.g = 0
        self.h = 0
        self.f = 0
        self.parent = None

    def __lt__(self, other):
        # We need to create a less than comparison as the heapq will use it to order
        # each cell. Without it the heapq has no idea how to compare the cells
        if isinstance(other, Cell):
            return self.f < other.f


class StarSearch(object):
    def __init__(self, world):
        # Init the search, we need to rebuild the set of cells as they need more info stored in them
        self.world = world
        self.opened = []
        heapq.heapify(self.opened)
        self.cells = [Cell(c, self.world) for c in self.world.cells]
        self.closed = set()
        self.start = self.cells[self.world.start]
        self.end = self.cells[self.world.end]
        # This may not be the best way to do this.
        for cell in self.cells:
            cell.populate_neighbors(self.world.maze_width, self.world.maze_height, self.cells)
            cell.draw_position = (cell.position[0] * (self.world.wall_width + self.world.path_width),
                                  cell.position[1] * (self.world.wall_width + self.world.path_width))

    def get_heuristic(self, cell):
        """
        Calculate the heuristic value H for a cell: dist between this cell and the ending cell x 10
        :param cell: the cell of which to calculate the heuristic
        :returns heuristic value:
        """
        return 10 * (abs(cell.position[1] - self.end.position[1]) + abs(cell.position[0] - self.end.position[0]))

    def get_path(self):
        # Iterates through the gathered cells by jumping to its parent
        # constructing a list of cells on the path between the start and end
        cell = self.end
        path = [cell]
        while cell.parent is not self.start:
            cell = cell.parent
            path.append(cell)
        path.append(self.start)
        path.reverse()
        return path

    def update_cell(self, adj, cell):
        """
        Updates a cells' heuristic and parent
        :param adj: The cell adjacent to the current cell to be updated
        :param cell: The current cell being evaluated
        :return: None
        """
        adj.g = cell.g + 10
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g

    def get_reachable(self, cell):
        """
        This iterates over all the neighbors of this cell and evaluates if a path could
        be made between them
        :param cell: The current cell being evaluated
        :return: A list of cardinal directions in clockwise order starting at north,
                    if the cell is not reachable it returns (False, None) for that cell
        """
        north = south = east = west = (False, None)
        for neighbor in cell.neighbors:
            if neighbor.id == cell.id - self.world.maze_width:
                north = (True if neighbor.path[1] else False, neighbor)
            elif neighbor.id == cell.id + self.world.maze_width:
                south = (True if cell.path[1] else False, neighbor)
            elif neighbor.id == cell.id - 1:
                west = (True if neighbor.path[0] else False, neighbor)
            elif neighbor.id == cell.id + 1:
                east = (True if cell.path[0] else False, neighbor)
        return [north, east, south, west]

    def solve(self):
        """
        The big worky worky bit
        Iterates over each cell, working with the most efficient path via the heapq sorting the
        lowest costing cell to the top to be evaluated next.
        This algo may need to be re-evaluated as it may be incomplete in its function
        It may not evaluate all possible paths, returning the most efficient
        (This was written over 3 years ago by myself as a first project to learn python)
        :return: (True, [path])
        """
        heapq.heappush(self.opened, (self.start.f, self.start))
        while len(self.opened):
            f, cell = heapq.heappop(self.opened)
            self.closed.add(cell)
            if cell is self.end:
                return True, self.get_path()
            neighbors = self.get_reachable(cell)
            for reachable, neighbor in neighbors:
                if reachable and neighbor not in self.closed:
                    if (neighbor.f, neighbor) in self.opened:
                        if neighbor.g > cell.g + 10:
                            self.update_cell(neighbor, cell)
                    else:
                        # Something isnt right here....?
                        self.update_cell(neighbor, cell)
                        heapq.heappush(self.opened, (neighbor.f, neighbor))
