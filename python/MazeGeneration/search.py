import heapq

from world import Cell as WorldCell


class Cell(WorldCell):
    def __init__(self, c, w):
        super().__init__(c.id, w.maze_width)
        self.path = c.path
        '''
        g = cost to move from the starting cell to this cell
        h = estimation of the cost to move from this cell to end cell
        f = g + h
        '''
        self.g = 0
        self.h = 0
        self.f = 0
        self.parent = None

    def __lt__(self, other):
        if isinstance(other, Cell):
            return self.f < other.f


class StarSearch(object):
    def __init__(self, world):
        self.world = world
        self.opened = []
        self.cells = [Cell(c, self.world) for c in self.world.cells]
        for cell in self.cells:
            cell.populate_neighbors(self.world.maze_width, self.world.maze_height, self.cells)
            cell.draw_position = (cell.position[0] * (self.world.wall_width + self.world.path_width),
                                  cell.position[1] * (self.world.wall_width + self.world.path_width))
        heapq.heapify(self.opened)
        self.closed = set()
        self.start = self.cells[self.world.start]
        self.end = self.cells[self.world.end]

    def get_heuristic(self, cell):
        """
        Calculate the heuristic value H for a cell :
        dist between this cell and the ending cell x 10
        #Takes param cell
        #returns heuristic val H
        """
        return 10 * (abs(cell.position[1] - self.end.position[1]) + abs(cell.position[0] - self.end.position[0]))

    def get_path(self):
        """
        Iterates through the gathered cells brow jumping to its parent
            then appending it to a list od tuples to be returned
        """
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
        :param adj:
        :param cell:
        :return:
        """
        adj.g = cell.g + 10
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g

    def get_reachable(self, cell):
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
        :return:
        """
        heapq.heappush(self.opened, (self.start.f, self.start))
        while len(self.opened):
            # Pop the top cell
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
