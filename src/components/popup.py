import pygame as pg

from paths import *

class Popup(pg.sprite.Sprite):

    IMAGE_PATHS = {'e_hint': IMAGE_DIR / 'e_hint.png'}

    containers = None
    images = {}

    def __init__(self, center):
        super().__init__(self.containers)
        self.image = self.images['e_hint']
        self.rect = self.image.get_rect(midbottom=center)
        self.rect.move_ip(0, -25)
        self.kill()

    def update(self, *args, **kwargs):
        pass

