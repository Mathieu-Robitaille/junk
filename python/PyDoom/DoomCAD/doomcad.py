from math import sqrt

import pygame as pg

"""
DoomCAD is 100% still in the "This is a rough prototype phase" so messy code is to be expected as
it is very possible I abandon this in favor of a 3D level editor. Especially if I migrate to pandas3D
for rendering in the future

As of Nov 22 2019, This project's code has grown to be very gross. Please do not look at my shame.  
"""

CLOSE = 4
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# Random keys, these are probably really bad picks, but i want to see the code actually work
# IF it works as i want, i can easily change these to a sensible set later
PAN_KEY = pg.K_LCTRL
RECTANGLE_KEY = pg.K_LSHIFT
CIRCLE_KEY = pg.K_c
SPLINE_KEY = pg.K_x
MOVE_NODE_BUTTON = 3


class DoomCAD:
    def __init__(self):
        if not pg.init():
            raise Exception("Could not init pygame")
        self.title = "DoomCAD"
        self.clock = pg.time.Clock()
        self.surface = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.end = (-1000000, -1000000)
        self.offset = (-SCREEN_WIDTH / 2, -SCREEN_HEIGHT / 2)
        self.start_offset = (0, 0)
        self.shape_move_offset = (0, 0)
        # Line, Rectangle, Circle, Splines
        self.shapes = [False] * 4
        self.mouse_pos = (0, 0)
        self.lines = []
        self.squares = []
        self.circles = []
        self.pan = False

    def draw(self):
        # Display  the center of the screen so we know where we are when panning
        pg.draw.circle(self.surface, pg.Color("white"), world_to_screen((0, 0), self.offset), 10)
        self.draw_lines()
        self.draw_squares()
        self.draw_circles()
        if self.end != (-1000000, -1000000):
            end = world_to_screen(self.end, self.offset)
            if self.shapes[0]:
                pg.draw.aaline(self.surface, pg.Color("Red"), end, self.mouse_pos)
            elif self.shapes[1]:
                pos = pg.mouse.get_pos()
                pg.draw.rect(self.surface, pg.Color("Red"), (end[0], end[1], pos[0] - end[0], pos[1] - end[1]), 5)
            elif self.shapes[2]:
                pos = pg.mouse.get_pos()
                r = dist(end, pos)
                pg.draw.circle(self.surface, pg.Color("Red"), (end[0], end[1]), r, width=5)
        if self.shape_move_offset != (0, 0):
            if self.shapes[2]:
                pos = pg.mouse.get_pos()
                r = dist(self.shape_move_offset, pos)
                pg.draw.circle(self.surface, pg.Color("Red"), pos, r, width=5)
        pg.display.update()

    def draw_lines(self):
        for line in self.lines:
            start = world_to_screen(line[0], self.offset)
            end = world_to_screen(line[1], self.offset)
            pg.draw.aaline(self.surface, pg.Color("White"), start, end)
            self.move_dot(start, end)

    def draw_squares(self):
        for rect in self.squares:
            x, y = world_to_screen((rect.x, rect.y), self.offset)
            w = rect.w
            h = rect.h
            pg.draw.rect(self.surface, pg.Color("Green"), (x, y, w, h), width=5)

    def draw_circles(self):
        for circle in self.circles:
            x, y = world_to_screen((circle.x, circle.y), self.offset)
            r = dist((circle.x, circle.y), (circle.w, circle.h))
            pg.draw.circle(self.surface, pg.Color("Purple"), (x, y), r, width=5)
            self.move_dot((x, y))

    def move_dot(self, start, end=(-1000000, -1000000)):
        if dist(start, pg.mouse.get_pos()) <= CLOSE:
            pg.draw.circle(self.surface, pg.Color("Red"), start, 5)
        if dist(end, pg.mouse.get_pos()) <= CLOSE:
            pg.draw.circle(self.surface, pg.Color("Red"), end, 5)

    def near_other_line(self):
        """
        :return: the dot you're near
        """
        pos = screen_to_world(pg.mouse.get_pos(), self.offset)
        for line in self.lines:
            if dist(line[0], pos) <= CLOSE:
                return line, line[1]
            if dist(line[1], pos) <= CLOSE:
                return line, line[0]
        return None

    def near_other_circle(self):
        pos = screen_to_world(pg.mouse.get_pos(), self.offset)
        for circle in self.circles:
            if dist((circle.x, circle.y), pos) <= CLOSE:
                return circle

    def toggle_keys(self):
        self.pan = False
        self.shapes = [False] * 4
        keys = pg.key.get_pressed()
        if keys != 0:
            self.pan = bool(keys[PAN_KEY])
            if not self.pan:
                self.shapes[0] = all(k == 0 for k in keys)
                # I'm thinking this should provide a priority to rectangle over other shapes
                self.shapes[1] = bool(keys[RECTANGLE_KEY] and all(s == False for s in self.shapes))
                self.shapes[2] = bool(keys[CIRCLE_KEY] and all(s == False for s in self.shapes))
                self.shapes[3] = bool(keys[SPLINE_KEY] and all(s == False for s in self.shapes))

    def event(self):
        """
        Wow this is bad and needs to get ripped out
        :return:
        """
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                self.start_offset = self.mouse_pos
            if pg.mouse.get_focused() and not self.pan:
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == MOVE_NODE_BUTTON and not CIRCLE_KEY:
                        near = self.near_other_line()
                        if near:
                            self.end = near[1]
                            if near[0] in self.lines:
                                self.lines.remove(near[0])
                    if event.button == MOVE_NODE_BUTTON and CIRCLE_KEY:
                        near = self.near_other_circle()
                        if near:
                            self.circles.remove(near)
                            self.shape_move_offset = (near.w, near.h)
                    # If we're drawing a shape
                    if event.button == 1:
                        if any(self.shapes):
                            self.end = screen_to_world(pg.mouse.get_pos(), self.offset)
                if event.type == pg.MOUSEBUTTONUP:
                    if self.end != (-1000000, -1000000):
                        if self.shapes[0]:
                            self.lines.append((self.end, screen_to_world(pg.mouse.get_pos(), self.offset)))
                        elif self.shapes[1]:
                            pos = screen_to_world(pg.mouse.get_pos(), self.offset)
                            self.squares.append(pg.Rect(self.end[0], self.end[1],
                                                        pos[0] - self.end[0], pos[1] - self.end[1]))
                        elif self.shapes[2]:
                            if self.shape_move_offset != (0, 0):
                                pos = screen_to_world(pg.mouse.get_pos(), self.offset)
                                self.circles.append(pg.Rect(pos[0], pos[1],
                                                            self.shape_move_offset[0], self.shape_move_offset[1]))
                            else:
                                pos = screen_to_world(pg.mouse.get_pos(), self.offset)
                                self.circles.append(pg.Rect(self.end[0], self.end[1],
                                                            pos[0], pos[1]))
                        self.end = (-1000000, -1000000)

    def do_pan(self):
        """ Naming 101 """
        if self.pan:
            self.offset = (self.offset[0] - (self.mouse_pos[0] - self.start_offset[0]),
                           self.offset[1] - (self.mouse_pos[1] - self.start_offset[1]))
            self.start_offset = self.mouse_pos
        else:
            self.start_offset = (0, 0)


def world_to_screen(world, offset):
    """
    :param world: world coords
    :param offset: offset value
    :return:
    """
    return world[0] - offset[0], world[1] - offset[1]


def screen_to_world(screen, offset):
    return screen[0] + offset[0], screen[1] + offset[1]


def dist(a, b):
    return sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)


class Wall:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.texture = ""

    def __iter__(self):
        for x in [self.p1, self.p2]:
            yield x


class Polygon:
    def __init__(self, lines):
        self.points = set([y for x in lines for y in x])


def main():
    cad = DoomCAD()
    while True:
        cad.clock.tick(60)
        cad.mouse_pos = pg.mouse.get_pos()
        cad.toggle_keys()
        cad.surface.fill(pg.Color("black"))
        cad.event()
        cad.do_pan()
        cad.draw()


if __name__ == "__main__":
    main()
