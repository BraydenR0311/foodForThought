import time

import pygame as pg

from paths import *
from src.utils.utils import get_screen_rect

class Player(pg.sprite.Sprite):
    IMAGE_PATHS = {
        'up': IMAGE_DIR / 'chef' / 'chef1.png',
        'walk1': IMAGE_DIR / 'chef' / 'chef2.png',
        'walk2': IMAGE_DIR / 'chef' / 'chef3.png'
    }

    images = {}
    animations = {}

    containers = None
    
    ANIM_SPEED = 0.2

    def __init__(self):
        super().__init__(self.containers)
        self.index = 0
        self.speed = 2
        self.dx = 0
        self.dy = 0
        self.image = self.images['up']
        self.rect = self.image.get_rect(center=get_screen_rect().center)
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

    #TODO: create class method to init animation (rotated images).
    @classmethod
    def set_additional_images(cls):
        """Image transformations and animations needed
        for this class."""
        new_images = {
            'down': pg.transform.rotate(cls.images['up'], 180),
            'left': pg.transform.rotate(cls.images['up'], 90),
            'right': pg.transform.rotate(cls.images['up'], 270),
        }

        animations = {
            'walk_up': [
                cls.images['walk1'], 
                cls.images['up'],
                cls.images['walk2'],
                cls.images['up']
            ],
            'walk_left': [
                pg.transform.rotate(cls.images['walk1'], 90), 
                new_images['left'],
                pg.transform.rotate(cls.images['walk2'], 90),
                new_images['left']
            ],
            'walk_right': [
                pg.transform.rotate(cls.images['walk1'], 270), 
                new_images['right'],
                pg.transform.rotate(cls.images['walk2'], 270),
                new_images['right']
            ],
            'walk_down': [
                pg.transform.rotate(cls.images['walk1'], 180), 
                new_images['down'],
                pg.transform.rotate(cls.images['walk2'], 180),
                new_images['down']
            ],
        }
        # Add to respective dictionary.
        cls.images.update(new_images)
        cls.animations.update(animations)




