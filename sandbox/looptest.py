import pygame as pg

pg.init()

screen = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()
running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    screen.fill('white')

    print(pg.time.get_ticks())

    pg.display.flip()
    clock.tick(60)

pg.quit()