from abc import ABC

import pygame as pg

from paths import *
from constants import *
from src.components.status import Popup

# Only inherited from.
class Tile(ABC):

    IMAGES = {
        '#': pg.image.load(IMAGE_DIR / 'floor.png').convert_alpha(),
        'x': pg.image.load(IMAGE_DIR / 'floor.png').convert_alpha(),
        'f': pg.image.load(IMAGE_DIR / 'fryer.png').convert_alpha(),
        'p': pg.image.load(IMAGE_DIR / 'pantry.png').convert_alpha(),
        'o': pg.image.load(IMAGE_DIR / 'oven.png').convert_alpha(),
        'c': pg.image.load(IMAGE_DIR / 'cutting.png').convert_alpha()
    }

    containers = None

    def __init__(self, kind: str, rect: pg.Rect):
        super().__init__()
        self.kind = kind
        # Will overwrite this rect immediately.
        self.image = self.IMAGES[self.kind]
        self.rect = rect
        if self.containers == None:
            raise ValueError('Must define groups for this class.')
        self.add(self.containers)

class Floor(Tile, pg.sprite.Sprite):
    def __init__(self, kind, rect):
        super().__init__(kind, rect)

class Appliance(Tile, pg.sprite.Sprite):

    def __init__(self, kind, rect):
        super().__init__(kind, rect)
        self.zone = self.rect.inflate(70, 70)
        self.popup = Popup(self.rect.center)
        self.center_vec = pg.math.Vector2(*self.rect.center)