from typing import override

import pygame as pg

from .. import config
from .menu import MENU, Ingredient
from .text import Quote, Text
from .generic import Generic
from enum import Enum, auto
from ..managers.visualmanager import VisualManager
from .tile import TileType, Tile
from dataclasses import dataclass
from pathlib import Path
import logging
from ..utils.image import Image, ImageCollection
from .. import groups

logger = logging.getLogger(__name__)

visual_manager = VisualManager()


class FoodState(Enum):
    UNFINISHED = auto()
    COOKED = auto()
    RUINED = auto()


@dataclass
class TicketIngredient:
    metadata: Ingredient
    food_coordinate: tuple[int, int]
    appliance_coordinate: tuple[int, int]
    status_coordinate: tuple[int, int]
    prepared: bool = False


class Ticket(pg.sprite.Sprite):
    """Manages QuoteSection and Food objects."""

    IMAGE_SIZE = 20
    containers = (groups.tickets, groups.all_sprites)

    images = ImageCollection(Image(config.IMAGE_DIR / "ticket" / "ticket.png"))

    def __init__(self, dish_name: str):
        super().__init__(*self.containers)
        self._dish_name = dish_name
        self._quote = Quote()
        self._grid = [
            [(30, 30), (60, 30), (90, 30)],
            [(30, 60), (60, 60), (90, 60)],
            [(30, 90), (60, 90), (90, 90)],
        ]
        self._ingredients = [
            TicketIngredient(
                ingredient,
                food_coordinate=self._grid[i][0],
                appliance_coordinate=self._grid[i][1],
                status_coordinate=self._grid[i][2],
            )
            for i, ingredient in enumerate(MENU[self._dish_name].ingredients)
        ]

        self._num_wrong = 0
        self._num_correct = 0
        # Topleft of each sprite.
        self._sprites = pg.sprite.Group()

        self.image = self.images.get_surface("ticket")

        # Position sprite.
        self.rect = self.image.get_rect(midtop=visual_manager.get_screen_rect().midtop)
        self.rect.move_ip(0, 10)

        self._author_image = self._quote.show_author_image(
            (300, 300), topleft=visual_manager.get_screen_rect().move(30, 30).topleft
        )

        self._author_name = Text(
            self._quote._author, 10, midtop=self._author_image.rect.move(0, 10).midbottom
        )

        # Display food.
        for ingredient in self._ingredients:
            self._sprites.add(
                Generic(
                    ingredient.metadata.image_path,
                    (Ticket.IMAGE_SIZE, Ticket.IMAGE_SIZE),
                    topleft=self.rect.move(ingredient.food_coordinate).topleft,
                )
            )
            self._sprites.add(
                Generic(
                    config.TILE_DIR
                    / f"{Tile.tile_type_to_image_name[ingredient.metadata.appliance]}.png",
                    (self.IMAGE_SIZE, self.IMAGE_SIZE),
                    topleft=self.rect.move(ingredient.appliance_coordinate).topleft,
                )
            )

        # Text object that is used on the ticket.
        self._sprites.add(
            Text(
                MENU[self._dish_name].name,
                8,
                "black",
                midbottom=self.rect.move(0, -12).midbottom,
            )
        )

        self._current_quote_section = None
        self._quote_section_sprites = []

    def update(self, *args, **kwargs):
        pass

    def get_cookable(self) -> TicketIngredient | None:
        return next(
            (ingredient for ingredient in self._ingredients if not ingredient.prepared),
            None,
        )

    def mark_wrong(self, ingredient_name: str):
        self._mark_finished(ingredient_name, config.TICKET_DIR / "x.png")
        self._num_wrong += 1

    def mark_correct(self, ingredient_name: str):
        self._mark_finished(ingredient_name, config.TICKET_DIR / "check.png")
        self._num_correct += 1

    def _mark_finished(self, ingredient_name: str, image_path: Path):
        """Returns True if successful."""
        ingredient = next(
            (
                ingredient
                for ingredient in self._ingredients
                if ingredient.metadata.name == ingredient_name
            ),
            None,
        )
        if not ingredient:
            logging.error("Cannot mark. Ingredient specified not found.")
            return

        self._sprites.add(
            Generic(
                image_path,
                (Ticket.IMAGE_SIZE, Ticket.IMAGE_SIZE),
                topleft=self.rect.move(ingredient.status_coordinate).topleft,
            )
        )
        ingredient.prepared = True
        self._quote_section_sprites.append(
            Text(
                self._current_quote_section,
                10,
                topleft=self._author_image.rect.move(
                    0, len(self._quote_section_sprites) * 10 + 50
                ).bottomleft,
            )
        )

    def pop(self):
        self._current_quote_section = self._quote.pop()
        return self._current_quote_section

    def is_done(self) -> bool:
        return not bool(len(self._quote))

    def get_dish_name(self):
        return self._dish_name

    def get_score(self) -> int:
        return self._num_correct

    @override
    def kill(self) -> None:
        """Player has finished all 3 quotes."""
        super().kill()
        for sprite in self._sprites.sprites():
            sprite.kill()
        for sprite in self._quote_section_sprites:
            sprite.kill()
        self._author_image.kill()
        self._author_name.kill()
