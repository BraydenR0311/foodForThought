import pygame as pg

from paths import *
from src.utils.utils import get_screen_rect


class Button(pg.sprite.Sprite):
    IMAGE_PATHS = {
        "play": IMAGE_DIR / "buttons" / "play.png",
        "quit": IMAGE_DIR / "buttons" / "quit.png",
    }

    containers = None
    images = {}

    def __init__(self, kind: str, center_loc: tuple[int, int]):
        super().__init__(self.containers)
        self.kind = kind
        self.image = self.images[self.kind]
        self.rect = self.image.get_rect()
        self.rect.center = center_loc
        self.clicked = False
        self.armed = False
        self.activated = False

    def is_activated(self):
        return self.activated

    def update(self, mouse_pos, click, *args, **kwargs):
        # If previously activated, deactivate.
        if self.activated:
            self.activated = False

        # Mouse hovering over self.
        armed = self.rect.collidepoint(mouse_pos)

        # Nothing done to self.
        if not armed and not click:
            self.armed = False
            self.unarm()
            self.clicked = False

        # Mouse is hovering.
        if armed and not self.armed:
            self.armed = True
            self.arm()

        # Hovering and left click held.
        if armed and click and not self.clicked:
            self.click()
            self.clicked = True

        # Activate self.
        if armed and not click and self.clicked:
            self.clicked = False
            self.activated = True

    def arm(self):
        self.image = pg.transform.hsl(self.image, lightness=-0.2)

    def unarm(self):
        self.image = self.images[self.kind]

    def click(self):
        self.image = pg.transform.hsl(self.image, lightness=-0.3)
