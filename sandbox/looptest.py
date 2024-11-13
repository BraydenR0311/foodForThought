import pygame as pg

pg.init()

screen = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()
running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN and event.key == pg.K_d:
            pg.event.
    screen.fill('white')

    pg.display.flip()
    clock.tick(60)

pg.quit()