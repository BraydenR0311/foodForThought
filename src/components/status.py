import pygame as pg

from paths import *

class Status(pg.sprite.Sprite):

    IMAGE_PATHS = {'check': IMAGE_DIR / 'check.png',
                   'x': IMAGE_DIR / 'x.png'}

    containers = None
    images = {}

    def __init__(self, isCheck):
        super().__init__(self.containers)
        self.image = self.images['check'] if isCheck else self.images['x']
        self.rect = self.image.get_rect()
    
    def make_wrong(self):
        self.image = self.images['x']

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
