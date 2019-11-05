import pygame as pg
from globals import SCREEN_WIDTH, LEVEL_HEIGHT, LEVEL_WIDTH, LEVEL_CELL_SPACING, FONT

pg.font.init()
font = pg.font.Font(FONT, 16)


def log(*msg):
    print(msg)


def on_screen_log(msg, surface):
    text = font.render(msg, True, pg.Color("Red"))
    text_rect = text.get_rect()
    text_rect.topleft = (SCREEN_WIDTH - (LEVEL_WIDTH * LEVEL_CELL_SPACING),
                         (LEVEL_HEIGHT + 1) * LEVEL_CELL_SPACING)
    surface.blit(text, text_rect)
