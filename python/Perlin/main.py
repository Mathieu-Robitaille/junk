import pygame as pg
from perlin import perlinoctave, perlin

width = 255

pg.init()
surface = pg.display.set_mode((width, width))
clock = pg.time.Clock()




while True:
    frame_time = clock.get_time() / 10
    for x in range(width):
        for y in range(width):
            print(frame_time)
            r = perlin(x, y, frame_time)
            g = perlin(x, y, frame_time)
            b = perlin(x, y, frame_time)
            pg.draw.circle(surface, (r, g, b), (x, y), 1)
    pg.display.update()
    clock.tick() # ticky boi???

