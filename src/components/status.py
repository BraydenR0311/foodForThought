import pygame as pg

from config import *


class Status(pg.sprite.Sprite):
    IMAGE_PATHS = {"check": IMAGE_DIR / "check.png", "x": IMAGE_DIR / "x.png"}

    containers = None
    images = {}

    def __init__(self, isCheck):
        super().__init__(self.containers)
        self.image = self.images["check"] if isCheck else self.images["x"]
        self.rect = self.image.get_rect()

    def make_wrong(self):
        self.image = self.images["x"]
