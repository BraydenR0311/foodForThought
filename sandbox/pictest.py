import pygame as pg
import time
from paths import *

pg.init()

screen = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()
running = True

class Player(pg.sprite.Sprite):

    up = pg.image.load(IMAGE_DIR / 'chef' / 'chef1.png')

    down = pg.transform.rotate(up, 180)

    left = pg.transform.rotate(up, 90)

    right = pg.transform.rotate(up, 270)

    walk_up = [
        pg.image.load(IMAGE_DIR / 'chef' / 'chef2.png'),
        up,
        pg.image.load(IMAGE_DIR / 'chef' / 'chef3.png'),
        up
    ]

    walk_down = [
        pg.transform.rotate(walk_up[0], 180),
        down,
        pg.transform.rotate(walk_up[2], 180),
        down
    ]

    walk_left = [
        pg.transform.rotate(walk_up[0], 90),
        left,
        pg.transform.rotate(walk_up[2], 90),
        left
    ]

    walk_right = [
        pg.transform.rotate(walk_up[0], 270),
        right,
        pg.transform.rotate(walk_up[2], 270),
        right
    ]

    ANIM_SPEED = 0.2

    def __init__(self):
        super().__init__()
        self.index = 0
        self.screen = pg.display.get_surface()
        self.speed = 2
        self.image = self.up
        self.rect = self.image.get_rect(center=screen.get_rect().center)
        self.time = time.time()
        
    
    def _animate(self, anim):
        self.elapsed = time.time() - self.time
        if self.elapsed > self.ANIM_SPEED:
            if self.index == len(anim):
                self.index = 0
            self.image = anim[self.index]
            self.time = time.time()
            self.index += 1

    def _move(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.walking = True
            self._animate(self.walk_up)
            self.rect.move_ip(0, -self.speed)
        if keys[pg.K_s]:
            self.walking = True
            self._animate(self.walk_down)
            self.rect.move_ip(0, self.speed)
        if keys[pg.K_a]:
            self.walking = True
            self._animate(self.walk_left)
            self.rect.move_ip(-self.speed, 0)
        if keys[pg.K_d]:
            self.walking = True
            self._animate(self.walk_right)
            self.rect.move_ip(self.speed, 0)
        

    def update(self, *args, **kwargs):
        self._move()

group = pg.sprite.Group()

surf = pg.image.load(IMAGE_DIR / 'oven.png')
rect = surf.get_rect()

x = 0
y = 500

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    screen.fill('white')

    screen.blit(surf, (500, 500, 200, 200), (x, 40, 20, 20))
    x += 1

    pg.display.flip()
    clock.tick(60)


pg.quit()