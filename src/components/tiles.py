from abc import ABC

import pygame as pg

from paths import *
from src.config import Config
from src.components.status import Popup

# Only inherited from.
class Tile(ABC):
    IMAGE_PATHS = {
        '#': IMAGE_DIR / 'floor.png',
        'x': IMAGE_DIR / 'floor.png',
        'f': IMAGE_DIR / 'fryer.png',
        'p': IMAGE_DIR / 'pantry.png',
        'o': IMAGE_DIR / 'oven.png',
        'c': IMAGE_DIR / 'cutting.png'
    }

    containers = None
    images = {}

    def __init__(self, kind: str, rect: pg.Rect):
        super().__init__()
        self.kind = kind
        # Will overwrite this rect immediately.
        self.image = self.images[self.kind]
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