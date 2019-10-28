import pygame as pg

from math import pi, cos, sin
from globals import TEAM_PLAYER, TEAM_ENEMY, two_d_to_one_d


class Entity:
    def __init__(self, pos, sprite, team, game):
        # This entity's position in X, Y
        self.pos = pos
        # This entity's facing angle
        self.angle = pi / 2

        # The players FOV
        self.fov = pi / 3

        # This entity's sprite (Image Utilities are not implemented yet)
        #self.sprite = iu.images[sprite]
        self.team = team

        # local variable for time between things
        self.tick = 0.0

        self.dead = False

        self.game = game

        # List for W, A, S, D
        self.wasd_held = [False, False, False, False]
        #
        self.health = 100

    def update(self):
        if self.health < 0:
            self.dead = True
        self.move()

    def do_damage(self, target, damagetype, amount):
        pass

    def take_damage(self, amount):
        pass

    def move(self):
        pass

    def event(self, event, timer):
        self.tick = timer

    def move_check(self, pos):
        return False if self.game.level.map[two_d_to_one_d(pos, self.game.level.width)].is_wall else True

class Enemy(Entity):
    def __init__(self, game):
        super().__init__(pos=(10.0, 10.0), sprite=None, team=TEAM_ENEMY, game=game)
        self.spottedplayer = False # ??? How are we going to handle attacking the player?

    def update(self):
        super().update()
        self.move()

    def do_damage(self, target, damage_type, amount):
        super().do_damage(target, damage_type, amount)
        pass

    def take_damage(self, amount):
        super().take_damage(amount)
        pass

    def move(self):
        super().move()


class Player(Entity):
    def __init__(self, game):
        super().__init__(pos=(3.0, 3.0), sprite=None, team=TEAM_PLAYER, game=game)

    def update(self):
        super().update()

    def do_damage(self, target, damagetype, amount):
        super().do_damage(target, damagetype, amount)
        pass

    def take_damage(self, amount):
        super().take_damage(amount)
        pass

    def move(self):
        if self.wasd_held[0]:
            tmp_pos = (self.pos[0] + (sin(self.angle) * 1.0 * self.tick),
                       self.pos[1] + (cos(self.angle) * 1.0 * self.tick))
            self.pos = tmp_pos if self.move_check(tmp_pos) else self.pos
            # print(self.pos, " -> ", tmp_pos)
        if self.wasd_held[1]:
            self.angle -= 1.0 * self.tick
        if self.wasd_held[2]:
            tmp_pos = (self.pos[0] - (sin(self.angle) * 1.0 * self.tick),
                       self.pos[1] - (cos(self.angle) * 1.0 * self.tick))
            self.pos = tmp_pos if self.move_check(tmp_pos) else self.pos
            # print(self.pos, " -> ", tmp_pos)
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
