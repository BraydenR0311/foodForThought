import pygame as pg

from paths import *
from constants import *

class Button(pg.sprite.Sprite):

    IMAGES = {'play': pg.image.load(IMAGE_DIR
                                    / 'buttons'
                                    / 'play.png').convert_alpha(),

              'quit': pg.image.load(IMAGE_DIR                                         
                                            / 'buttons'
                                            / 'quit.png').convert_alpha()}

    containers = None

    def __init__(self, kind: str):
        super().__init__(self.containers)
        self.kind = kind
        self.image = self.IMAGES[self.kind]
        self.rect = self.align_rect()
        self.clicked = False
        self.armed = False

    def align_rect(self) -> pg.Rect:
        rect = self.image.get_rect()
        rect.center = SCREEN_RECT.center

        distance = 150
        if self.kind == 'play':
            rect.move_ip(pg.transform.hsl(self.image, lightness = -.2))

    def unarm(self):
        self.image = self.IMAGES[self.kind]

    def click(self):
        self.image = pg.transform.hsl(self.image, lightness = -.3)