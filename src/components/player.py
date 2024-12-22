import time

import pygame as pg

from paths import *
from constants import *

class Player(pg.sprite.Sprite):

    up_still = pg.image.load(IMAGE_DIR / 'chef' / 'chef1.png').convert_alpha()

    down_still = pg.transform.rotate(up_still, 180)

    left_still = pg.transform.rotate(up_still, 90)

    right_still = pg.transform.rotate(up_still, 270)

    walk_up = [
        pg.image.load(IMAGE_DIR / 'chef' / 'chef2.png').convert_alpha(),
        up_still,
        pg.image.load(IMAGE_DIR / 'chef' / 'chef3.png').convert_alpha(),
        up_still
    ]

    walk_down = [
        pg.transform.rotate(walk_up[0], 180),
        down_still,
        pg.transform.rotate(walk_up[2], 180),
        down_still
    ]

    walk_left = [
        pg.transform.rotate(walk_up[0], 90),
        left_still,
        pg.transform.rotate(walk_up[2], 90),
        left_still
    ]

    walk_right = [
        pg.transform.rotate(walk_up[0], 270),
        right_still,
        pg.transform.rotate(walk_up[2], 270),
        right_still
    ]

    ANIM_SPEED = 0.2

    containers = None

    def __init__(self):
        super().__init__(self.containers)
        self.index = 0
        self.screen = pg.display.get_surface()
        self.speed = 2
        self.dx = 0
        self.dy = 0
        self.image = self.up_still
        self.rect = self.image.get_rect(center=self.screen.get_rect().center)
        self.time = time.time()

    def update(self):
        self.center_vec = pg.math.Vector2(*self.rect.center)

    def animate(self, anim):
        self.elapsed = time.time() - self.time
        if self.elapsed > self.ANIM_SPEED:
            if self.index == len(anim):
                self.index = 0
            self.image = anim[self.index]
            self.time = time.time()
            self.index += 1
