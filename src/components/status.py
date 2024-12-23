import pygame as pg

from paths import *

class Status(pg.sprite.Sprite):

    IMAGES = {'check': pg.image.load(IMAGE_DIR / 'check.png'),
              'x': pg.image.load(IMAGE_DIR / 'x.png')}

    containers = None

    def __init__(self, isCheck):
        super().__init__(self.containers)
        if isCheck:
            self.image = self.IMAGES['check']
        else:
            self.image = self.IMAGES['x']
        self.rect = self.image.get_rect()

class Popup(pg.sprite.Sprite):

    IMAGE = pg.image.load(IMAGE_DIR / 'e_hint.png').convert_alpha()

    containers = None

    def __init__(self, center):
        super().__init__(self.containers)
        self.image = self.IMAGE
        self.rect = self.image.get_rect(midbottom=center)
        self.rect.move_ip(0, -25)
        self.kill()

    def update(self):
        pass
