from typing import override

import pygame as pg

from .. import config
from ..common import MENU
from .food import Food, FoodState
from .tile import Table
from .text import Quote, Text
from ..utils.utils import get_screen_rect


class Ticket(pg.sprite.Sprite):
    """Manages QuoteSection and Food objects."""

    # First element(s) from top will be pushed down 30px.
    FIRST_OFFSET = 30
    # Offset for the rest of the elements displayed on the ticket.
    SUBOFFSET = 10

    IMAGE_PATHS = {"ticket": config.IMAGE_DIR / "ticket" / "ticket.png"}

    containers = None
    images = {}

    def __init__(self, dish_name):
        super().__init__(self.containers)
        self.dish_name = dish_name
        self._quote = Quote()

        # Text object that is used on the ticket.
        self.dish_name_text = Text(self.dish_name, 8, "black")
        self.ingredients = self._set_ingredients()
        self.num_correct = 0

        self._table = None

        self.image = self.images["ticket"]
        self.rect = self.image.get_rect()

        # Position self and items.
        self._position_items()

    def update(self, *args, **kwargs):
        pass

    def belongs_to(self, table: Table) -> bool:
        return table is self._table

    @property
    def quote(self) -> Quote:
        return self._quote

    def is_done(self) -> bool:
        return bool(len(self.quote))

    def get_score(self) -> int:
        return sum(ingr.get_state() == FoodState.COOKED for ingr in self.ingredients)

    def get_unfinished(self):
        return [
            ingr
            for ingr in self.ingredients
            if ingr.get_state() == FoodState.UNFINISHED
        ]

    def _set_ingredients(self) -> list[Food]:
        """Create Food objects based on the dish and its ingredients."""
        return [Food(ingredient) for ingredient in MENU[self.dish_name]]

    @override
    def kill(self) -> None:
        """Player has finished all 3 quotes."""
        super().kill()
        for ingredient in self.ingredients:
            ingredient.kill()
            ingredient.appliance_hint.kill()
            ingredient.status.kill()

    def _position_items(self):
        """Position self and objects within self."""
        # Position self.
        self.rect.midtop = get_screen_rect().midtop
        self.rect.move_ip(0, self.SUBOFFSET)

        # Position ingredients.
        previous_ingredient = None
        for ingredient in self.ingredients:
            # Position first ingredient.
            if not previous_ingredient:
                # Match topleft corners.
                ingredient.rect.topleft = self.rect.topleft
                # Offset first ingredient.
                ingredient.rect.move_ip(self.SUBOFFSET, self.FIRST_OFFSET)
            else:
                # Match topleft corner to bottom left of previous ingredient.
                ingredient.rect.topleft = previous_ingredient.rect.bottomleft
                ingredient.rect.move_ip(0, self.SUBOFFSET)

            ingredient.appliance_hint.rect.midleft = ingredient.rect.midright
            ingredient.appliance_hint.rect.move_ip(self.SUBOFFSET, 0)

            previous_ingredient = ingredient

            self.dish_name_text.rect.bottomleft = self.rect.bottomleft
            self.dish_name_text.rect.move_ip(self.SUBOFFSET, -self.SUBOFFSET)
