import pygame as pg
from pathlib import Path


class Generic(pg.sprite.Sprite):
    """For any type of image that needs to be blitted onto the screen, but
    wrapped in a class for sprite interface.

    No extra functionality.
    """

    containers = None
    images = {}

    def __init__(self, image_path: str | Path):
        super().__init__(self.containers)
        self.image = pg.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()

    def change_image(self, image) -> None:
        self.image = image
