from math import sqrt

import pygame as pg

"""
DoomCAD is 100% still in the "This is a rough prototype phase" so messy code is to be expected as
it is very possible I abandon this in favor of a 3D level editor. Especially if I migrate to pandas3D
for rendering in the future
"""

CLOSE = 4
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PAN_KEY = pg.K_LCTRL
RECTANGLE_KEY = pg.K_LSHIFT
CIRCLE_KEY = pg.K_c


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
        # Line, Rectangle, Circle, Splines
        self.shapes = [False, False, False, False]
        self.mouse_pos = (0, 0)
        self.lines = []
        self.squares = []
        self.circles = []
        self.pan = False

    def draw(self):
        if self.shapes[1]:
            pg.draw.circle(self.surface, pg.Color("White"), pg.mouse.get_pos(), 20)
        pg.draw.circle(self.surface, pg.Color("white"), world_to_screen((0, 0), self.offset), 10)
        for line in self.lines:
            start = world_to_screen(line[0], self.offset)
            end = world_to_screen(line[1], self.offset)
            pg.draw.aaline(self.surface, pg.Color("White"), start, end)
            if dist(start, pg.mouse.get_pos()) <= CLOSE:
                pg.draw.circle(self.surface, pg.Color("Red"), start, 3)
            if dist(end, pg.mouse.get_pos()) <= CLOSE:
                pg.draw.circle(self.surface, pg.Color("Red"), end, 3)
        for rect in self.squares:
            x, y = world_to_screen((rect.x, rect.y), self.offset)
            w = rect.w
            h = rect.h
            pg.draw.rect(self.surface, pg.Color("Green"), (x, y, w, h), width=5)
        for circle in self.circles:
            x, y = world_to_screen((circle.x, circle.y), self.offset)
            r = dist((x, y), (circle.w, circle.h))
            pg.draw.circle(self.surface, pg.Color("Purple"), (x, y), r, width=5)
        if self.end != (-1000000, -1000000):
            end = world_to_screen(self.end, self.offset)
            if self.shapes[0]:
                pg.draw.aaline(self.surface, pg.Color("Red"), end, self.mouse_pos)
            elif self.shapes[1]:
                pos = pg.mouse.get_pos()
                pg.draw.rect(self.surface, pg.Color("Red"), (end[0], end[1], pos[0] - end[0], pos[1] - end[1]), 5)

        pg.display.update()

    def near_other(self):
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

    def event(self):
        for event in pg.event.get():
            self.pan = False
            keys = pg.key.get_pressed()
            if event.type == pg.KEYDOWN:
                self.start_offset = self.mouse_pos
            if keys != 0:
                if keys[PAN_KEY]:
                    self.pan = True
            else:
                self.shapes[1:] = False
            if pg.mouse.get_focused() and not self.pan:
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        near = self.near_other()
                        if near:
                            self.end = near[1]
                            if near[0] in self.lines:
                                self.lines.remove(near[0])
                    if event.button == 1:
                        if all(k == 0 for k in keys):
                            self.shapes[0] = True
                        elif keys[RECTANGLE_KEY]:
                            self.shapes[1] = True
                        elif keys[CIRCLE_KEY]:
                            self.shapes[2] = True
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
                            self.shapes[1] = False
                        elif self.shapes[2]:
                            pos = screen_to_world(pg.mouse.get_pos(), self.offset)
                            self.circles.append(pg.Rect(self.end[0], self.end[1],
                                                        pos[0] - self.end[0], pos[1] - self.end[1]))
                            self.shapes[2] = False
                        self.end = (-1000000, -1000000)


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
        cad.surface.fill(pg.Color("black"))
        cad.event()
        if cad.pan:
            cad.offset = (cad.offset[0] - (cad.mouse_pos[0] - cad.start_offset[0]),
                          cad.offset[1] - (cad.mouse_pos[1] - cad.start_offset[1]))
            cad.start_offset = cad.mouse_pos
        cad.draw()


if __name__ == "__main__":
    main()
