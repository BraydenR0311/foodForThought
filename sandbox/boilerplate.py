import pygame as pg

pg.init()

screen = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()
running = True
keys = pg.key.get_pressed()

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    screen.fill('white')

    pg.display.flip()
    clock.tick(60)

pg.quit()