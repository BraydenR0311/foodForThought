import pygame as pg
from .. import groups
from ..utils.image import Image, ImageCollection

from .generic import Generic
from .. import config
import math

from enum import Enum


class Popup(pg.sprite.Sprite):
    SYMBOL_SIZE = 30

    containers = (groups.popups, groups.all_sprites)
    images = ImageCollection(
        Image(config.POPUP_DIR / "popupBackground.png"),
    )

    def __init__(self, center, symbol):
        super().__init__(*self.containers)
        self.image = self.images.get_surface("popupBackground")
        self.rect = self.image.get_rect(midbottom=center)
        self.rect.move_ip(0, -25)

        self.initial_y = self.rect.y
        self.start = pg.time.get_ticks()

        self.symbols = {
            "e": lambda: Generic(
                config.POPUP_DIR / "e.png", (Popup.SYMBOL_SIZE, Popup.SYMBOL_SIZE)
            ),
            "ready": lambda: Generic(
                config.POPUP_DIR / "ready.png", (Popup.SYMBOL_SIZE, Popup.SYMBOL_SIZE)
            ),
            "waiting": lambda: Generic(
                config.POPUP_DIR / "waiting.png", (Popup.SYMBOL_SIZE, Popup.SYMBOL_SIZE)
            ),
        }

        self.symbol = self.symbols[symbol]()

    def update(self, elapsed, *args, **kwargs):
        self._animate(elapsed - self.start)
        self.symbol.rect.center = self.rect.center
        self.symbol.rect.move_ip(0, -12)

    def kill(self):
        super().kill()
        self.symbol.kill()

    def change_symbol(self, symbol: str):
        self.symbol.kill()
        self.symbol = self.symbols[symbol]()

    def _animate(self, elapsed):
        sin_val = math.sin(elapsed / 300) * 10
        self.rect.y = self.initial_y + sin_val
