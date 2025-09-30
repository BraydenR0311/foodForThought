import pygame as pg

from config import *
from src.common import TILE_IMAGE_PATHS
from src.components.generic import Generic


class Food(pg.sprite.Sprite):
    IMAGE_PATHS = {
        "burger": FOOD_DIR / "burger.png",
        "cheese": FOOD_DIR / "cheese.png",
        "patty": FOOD_DIR / "patty.png",
        "bun": FOOD_DIR / "bun.png",
        "patty": FOOD_DIR / "patty.png",
        "taco": FOOD_DIR / "taco.png",
        "beef": FOOD_DIR / "beef.png",
        "shell": FOOD_DIR / "shell.png",
        "tomato": FOOD_DIR / "tomato.png",
    } | TILE_IMAGE_PATHS  # Concatenate dictionaries

    APPLIANCE_DICT = {
        "burger": None,
        "cheese": "c",
        "patty": "o",
        "bun": "o",
        "taco": None,
        "beef": "o",
        "tomato": "c",
        "shell": "o",
    }

    containers = None
    images = {}

    def __init__(self, kind):
        super().__init__(self.containers)
        # What ingredient/dish this is.
        self.kind = kind
        # Sprite object: Green check if correct, red if incorrect.
        self.status_sprite = None
        # What appliance is this dish cooked on.
        self.appliance = self.APPLIANCE_DICT[self.kind]
        # Dishes don't have an appliance, only ingredients.
        if self.appliance:
            self.appliance_hint = Generic(self.IMAGE_PATHS[self.appliance])
            self.appliance_hint.image = pg.transform.scale_by(
                self.appliance_hint.image, 0.25
            )
            self.appliance_hint.rect = self.appliance_hint.image.get_rect()

        self.image = self.images[self.kind]
        self.rect = self.image.get_rect()

    def finish_correctly(self):
        self.status = Generic(IMAGE_DIR / "check.png")

    def finish_incorrectly(self):
        self.status = Generic(IMAGE_DIR / "x.png")
