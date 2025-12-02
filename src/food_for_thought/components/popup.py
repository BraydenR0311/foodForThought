import pygame as pg
from .. import groups
from ..utils.image import Image, ImageCollection

from .. import config
import math


class Popup(pg.sprite.Sprite):
    containers = (groups.popups, groups.all_sprites)
    images = ImageCollection(Image(config.POPUP_DIR / "popupBackground.png"))

    def __init__(self, center):
        super().__init__(*self.containers)
        self.image = self.images.get_surface("popupBackground")
        self.rect = self.image.get_rect(midbottom=center)
        self.rect.move_ip(0, -25)

        self.initial_y = self.rect.y
        self.start = pg.time.get_ticks()

    def update(self, elapsed, *args, **kwargs):
        self._animate(elapsed - self.start)

    def _animate(self, elapsed):
        sin_val = math.sin(elapsed / 300) * 10
        self.rect.y = self.initial_y + sin_val
