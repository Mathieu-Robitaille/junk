import pygame as pg

from math import pi, cos, sin
from globals import PLAYER_TEAM


class Entity:
    def __init__(self, pos, sprite, team):
        # This entity's position
        self.pos = pos
        # This entity's facing angle
        self.angle = pi / 2

        # The players FOV
        self.fov = pi / 4

        # This entity's sprite (Image Utilities are not implemented yet)
        #self.sprite = iu.images[sprite]
        self.team = team

        # local variable for time between things
        self.tick = 0.0

        self.dead = False

        # List for W, A, S, D
        self.wasd_held = [False, False, False, False]
        #
        self.health = 100

    def update(self):
        if self.health < 0:
            self.dead = True
        self.move()

    def do_damage(self, target, amount):
        pass

    def take_damage(self, amount):
        pass

    def move(self):
        pass

    def event(self, event, timer):
        self.tick = timer


class Player(Entity):
    def __init__(self):
        super().__init__((3.0, 3.0), None, PLAYER_TEAM)

    def do_damage(self, target, amount):
        pass

    def damage(self):
        pass

    def move(self):
        if self.wasd_held[0]:
            self.pos = (self.pos[0] + (sin(self.angle) * 1.0 * self.tick),
                        self.pos[1] + (cos(self.angle) * 1.0 * self.tick))
        if self.wasd_held[1]:
            self.angle -= 1.0 * self.tick
        if self.wasd_held[2]:
            self.pos = (self.pos[0] - (sin(self.angle) * 1.0 * self.tick),
                        self.pos[1] - (cos(self.angle) * 1.0 * self.tick))
        if self.wasd_held[3]:
            self.angle += 1.0 * self.tick

    def event(self, event, timer):
        super().event(event, timer)
        if event.type in (pg.KEYDOWN, pg.KEYUP):
            if event.key == pg.K_w:
                self.wasd_held[0] = not self.wasd_held[0]
            if event.key == pg.K_a:
                self.wasd_held[1] = not self.wasd_held[1]
            if event.key == pg.K_s:
                self.wasd_held[2] = not self.wasd_held[2]
            if event.key == pg.K_d:
                self.wasd_held[3] = not self.wasd_held[3]
