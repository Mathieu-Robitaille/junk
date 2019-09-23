from pydoom import PyDoom
from render_manager import *


class Menu(PyDoom):
    def __init__(self):
        super().__init__()

    def draw(self, surface):
        for i in points_in_circum(300, 100):
            pg.draw.circle(surface, pg.Color("green"), (int(i[0]), int(i[1])), 1)

    def event(self, event):
        pass
