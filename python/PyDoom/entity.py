import pygame as pg

from math import pi
from globals import PLAYER_TEAM


class Entity:
    def __init__(self, pos, sprite, team):
        # This entity's position
        self.pos = pos
        # This entity's facing angle
        self.angle = pi / 2
        #
        self.fov = pi / 4
        # This entity's sprite (Image Utilities are not implemented yet)
        #self.sprite = iu.images[sprite]
        self.team = team

        #
        self.health = 100

    def do_damage(self, target, amount):
        pass

    def take_damage(self, amount):
        pass

    def move(self):
        pass


class Player(Entity):
    def __init__(self):
        super().__init__((3.0, 3.0), None, PLAYER_TEAM)

    def do_damage(self, target, amount):
        pass

    def damage(self):
        pass

    def move(self, direction="forward", amount=0.1):
        if direction == "forward":
            self.pos = (self.pos[0], self.pos[1] + amount)
        if direction == "left":
            self.angle -= 0.1
        if direction == "back":
            self.pos = (self.pos[0], self.pos[1] - amount)
        if direction == "right":
            self.angle += 0.1

    def event(self, event):
        if event.key == pg.K_w:
            self.move("forward")
        if event.key == pg.K_a:
            self.move("left")
        if event.key == pg.K_s:
            self.move("back")
        if event.key == pg.K_d:
            self.move("right")
