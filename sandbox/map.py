import pygame as pg
from paths import *



with open(ROOT_DIR / 'map1', 'r', encoding='utf-8') as infile:
    map = infile.read().splitlines()

class Tile(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load(IMAGE_DIR / 'floor.png')
        self.rect = self.image.get_rect()

pg.init()

# class map:
#     def __init__(self):
#         pass
#     def read(self):
#         raw_map = 

screen = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()
running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    screen.fill('white')

    pg.display.flip()
    clock.tick(60)

pg.quit()