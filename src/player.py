import pygame as pg
import time
from constants import *
from paths import *

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

    def __init__(self, collide_group, kitchen):
        super().__init__()
        self.collide_group = collide_group
        self.kitchen = kitchen
        self.index = 0
        self.screen = pg.display.get_surface()
        self.speed = 2
        self.dx = 0
        self.dy = 0
        self.image = self.up
        self.rect = self.image.get_rect(center=self.screen.get_rect().center)
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
        self.dx = 0
        self.dy = 0
        if keys[pg.K_LSHIFT]:
            self.speed = 4
        else:
            self.speed = 2
        
        
        if keys[pg.K_w]:
            self.dy = -self.speed
            self._animate(self.walk_up)
            self.rect.move_ip(0, self.dy)
        if keys[pg.K_s]:
            self.dy = self.speed
            self._animate(self.walk_down)
            self.rect.move_ip(0, self.dy)
        
        hitlist = pg.sprite.spritecollide(self, self.collide_group, False)
        for sprite in hitlist:
            if self.dy > 0:
                self.rect.bottom = sprite.rect.top
            elif self.dy < 0:
                self.rect.top = sprite.rect.bottom

        if keys[pg.K_a]:
            self.dx = -self.speed
            self._animate(self.walk_left)
            self.rect.move_ip(self.dx, 0)
        if keys[pg.K_d]:
            self.dx = self.speed
            self._animate(self.walk_right)
            self.rect.move_ip(self.dx, 0)

        hitlist = pg.sprite.spritecollide(self, self.collide_group, False)
        for sprite in hitlist:
            if self.dx > 0:
                self.rect.right = sprite.rect.left 
            elif self.dx < 0:
                self.rect.left = sprite.rect.right

    def update(self):
        self._move()
        self.rect = self.rect.clamp(self.kitchen.rect)