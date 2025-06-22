from enum import Enum, auto
from typing import override
import pygame as pg

from .. import config
from ..components.status import Status
from ..components.generic import Generic
from ..common import TILE_IMAGE_PATHS


class FoodState(Enum):
    UNFINISHED = auto()
    COOKED = auto()
    RUINED = auto()


class Food(pg.sprite.Sprite):
    IMAGE_PATHS = {
        "burger": config.FOOD_DIR / "burger.png",
        "cheese": config.FOOD_DIR / "cheese.png",
        "patty": config.FOOD_DIR / "patty.png",
        "bun": config.FOOD_DIR / "bun.png",
        "taco": config.FOOD_DIR / "taco.png",
        "beef": config.FOOD_DIR / "beef.png",
        "shell": config.FOOD_DIR / "shell.png",
        "tomato": config.FOOD_DIR / "tomato.png",
    }
    IMAGE_PATHS.update(TILE_IMAGE_PATHS)

    APPLIANCE_DICT = {
        "cheese": "c",
        "patty": "o",
        "bun": "o",
        "beef": "o",
        "tomato": "c",
        "shell": "o",
    }

    containers = None
    images = {}

    def __init__(self, kind):
        super().__init__(self.containers)
        # What ingredient/dish this is.
        self._kind = kind
        # Sprite object: Green check if correct, red if incorrect.
        self._status = Status()
        self._state = FoodState.UNFINISHED
        # What appliance the ingredient is cooked on.
        # Returns None if it doesn't have an appliance (ie. dishes).
        self._appliance = self.APPLIANCE_DICT.get(self._kind)
        # Dishes don't have an appliance, only ingredients.
        if self._appliance is not None:
            self.appliance_hint = Generic(self.IMAGE_PATHS[self._appliance])
            self.appliance_hint.image = pg.transform.scale_by(
                self.appliance_hint.image, 0.25
            )
            self.appliance_hint.rect = self.appliance_hint.image.get_rect()

        self.image = self.images[self._kind]
        self.rect = self.image.get_rect()

    @override
    def kill(self) -> None:
        super().kill()
        self._status.kill()
        if self.appliance_hint:
            self._appliance_hint.kill()

    def get_kind(self) -> str:
        return self._kind

    def get_state(self) -> FoodState:
        return self._state

    def finish_cooked(self):
        self._status.make_correct()
        self._state = FoodState.COOKED

    def finish_ruined(self):
        self._status.make_wrong()
        self._state = FoodState.RUINED
