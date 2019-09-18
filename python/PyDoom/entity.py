from globals import PLAYER_TEAM
import pygame as pg


class Entity():
    def __init__(self, pos, sprite, team):
        self.pos = pos
        # self.sprite = iu.images[sprite]
        self.team = team

    def do_damage(self, target):
        pass

    def damage(self):
        pass

    def move(self):
        pass


class Player(Entity):
    def __init__(self):
        super().__init__((1.0, 1.0), None, PLAYER_TEAM)
        self.health = 100

    def do_damage(self, target):
        pass

    def damage(self):
        pass

    def move(self):
        pass

    def event(self, event):
        if event.key == pg.K_w:
            pass
        if event.key == pg.K_a:
            pass
        if event.key == pg.K_s:
            pass
        if event.key == pg.K_d:
            pass
