import pygame as pg

from .. import config


class Status(pg.sprite.Sprite):
    IMAGE_PATHS = {
        "check": config.TICKET_DIR / "check.png",
        "x": config.TICKET_DIR / "x.png",
    }

    containers = None
    images = {}

    def __init__(self):
        super().__init__()
        self.image = self.images["check"]
        self.rect = self.image.get_rect()

    def make_wrong(self):
        self.add(self.containers)
        self.image = self.images["x"]

    def make_correct(self):
        self.add(self.containers)
        self.image = self.images["check"]
