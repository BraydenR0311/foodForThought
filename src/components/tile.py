from abc import ABC
import random

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
        'c': IMAGE_DIR / 'cutting.png',
        't': IMAGE_DIR / 'table.png'
    }

    containers = None
    images = {}

    def __init__(self, kind: str, rect: pg.Rect):
        super().__init__()
        self.kind = kind
        self.image = self.images[self.kind]
        # Will overwrite this rect immediately.
        self.rect = rect
        if self.containers == None:
            raise ValueError('Must define groups for this class.')
        self.add(self.containers)

    @classmethod
    def get_images(cls) -> dict[str, pg.Surface]:
        return cls.images

class Floor(Tile, pg.sprite.Sprite):
    def __init__(self, kind, rect):
        super().__init__(kind, rect)

class Appliance(Tile, pg.sprite.Sprite):
    def __init__(self, kind, rect):
        super().__init__(kind, rect)
        self.zone = self.rect.inflate(70, 70)
        self.popup = Popup(self.rect.center)
        self.center_vec = pg.math.Vector2(*self.rect.center)

class Table(Appliance, pg.sprite.Sprite):
    order_cooldown = 15
    max_order_time = 30
    def __init__(self, kind, rect, dish_names):
        super().__init__(kind, rect)
        self.player_rect = None
        self.keys = None
        self.is_closest = False
        self.elapsed = 0
        self.time_since_order = 0
        self.dish_names = dish_names

    def update(self, elapsed, player_rect, keys, closest, *args, **kwargs):
        self.elapsed = elapsed
        self.player_rect = player_rect
        self.keys = keys
        if self is closest:
            is_closest = True

    def order(self):
        dish = random.choice(self.dish_names)
        self.popup.add(Popup.containers)
  