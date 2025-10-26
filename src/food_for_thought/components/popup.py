import pygame as pg

from .. import config
import math


class Popup(pg.sprite.Sprite):
    IMAGE_PATHS = {"e_hint": config.POPUP_DIR / "e_hint.png"}

    containers = None
    images = {}

    def __init__(self, center):
        super().__init__(self.containers)
        self.image = self.images["e_hint"]
        self.rect = self.image.get_rect(midbottom=center)
        self.rect.move_ip(0, -25)

        self.initial_y = self.rect.y
        self.start = pg.time.get_ticks()

    def update(self, elapsed, *args, **kwargs):
        print(self.start)
        self.animate(elapsed - self.start)

    def animate(self, elapsed):
        sin_val = math.sin(elapsed / 300) * 10
        self.rect.y = self.initial_y + sin_val
