import pygame as pg

from paths import *
from utils.utils import get_screen_rect

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

    # TODO: don't return, just directly access rect
    def align_rect(self) -> pg.Rect:
        rect = self.image.get_rect()
        rect.center = get_screen_rect().center

        distance = 150
        if self.kind == 'play':
            rect.move_ip(0, -distance)
        if self.kind == 'quit':
            rect.move_ip(0, distance)
        return rect
    
    def arm(self):
        self.image = pg.transform.hsl(self.image, lightness = -.2)

    def unarm(self):
        self.image = self.IMAGES[self.kind]

    def click(self):
        self.image = pg.transform.hsl(self.image, lightness = -.3)
