import pygame as pg
from paths import *
from constants import *
from src.kitchen import Kitchen
from src.player import Player

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

background = pg.image.load(IMAGE_DIR / 'background.png')

all_sprites = pg.sprite.Group()
players = pg.sprite.Group()
appliances = pg.sprite.Group()
kitchen = Kitchen(appliances)
player = Player(appliances, kitchen)

players.add(player)
all_sprites.add(kitchen.sprites(), player)

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.blit(background)
    all_sprites.draw(screen)
    all_sprites.update()

    for sprite in appliances.sprites():
        if sprite.hitbox.colliderect(player.rect):
            print(sprite.rect)
        else:
            print(False)

    pg.display.flip()
    clock.tick(60)

pg.quit()