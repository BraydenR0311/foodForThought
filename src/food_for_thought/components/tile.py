import random
from abc import ABC

import pygame as pg


from ..common import MENU, TILE_IMAGE_PATHS, APPLIANCE_DICT
from ..components.food import Food
from ..managers.gamestatemanager import GameStateManager
from ..managers.audiomanager import AudioManager
from ..gamestates.statekey import StateKey
from .popup import Popup

gamestate_manager = GameStateManager()
audio_manager = AudioManager()


# Only inherited from.
class Tile(pg.sprite.Sprite, ABC):
    IMAGE_PATHS = TILE_IMAGE_PATHS

    containers = None
    images = {}

    def __init__(self, kind: str, rect: pg.Rect):
        super().__init__()
        self.kind = kind
        self.image = self.images[self.kind]
        # Will overwrite this rect immediately.
        self.rect = rect
        if not self.containers:
            raise ValueError("Must define groups for this class.")
        self.add(self.containers)


class Floor(Tile):
    def __init__(self, kind: str, rect: pg.Rect):
        super().__init__(kind, rect)


class InteractTile(Tile):
    def __init__(
        self,
        kind: str,
        rect: pg.Rect,
    ):
        super().__init__(kind, rect)
        # Define the allowable area for player interaction.
        self._interaction_rect = self.rect.inflate(70, 70)
        self.popup = None
        self.center = pg.math.Vector2(*self.rect.center)

    def update(self, *args, **kwargs): ...

    def interact(self, player): ...

    def get_interaction_rect(self) -> pg.Rect:
        """Return the area where the user can interact."""
        return self._interaction_rect

    def show_interaction_popup(self):
        self.popup = Popup(self.rect.center)

    def unshow_interaction_popup(self):
        if self.popup is not None:
            self.popup.kill()


class Appliance(InteractTile):
    def __init__(
        self,
        kind: str,
        rect: pg.Rect,
    ):
        super().__init__(kind, rect)

    def can_cook(self, kind: str) -> bool:
        return self.kind == APPLIANCE_DICT[kind]

    def interact(self, player):
        if not player.has_order():
            return
        for ingredient in player.get_ticket().get_unfinished():
            if self.can_cook(ingredient):
                gamestate_manager.goto(StateKey.COOK, {""})


class Table(InteractTile):
    _tables = []
    # Will leave at this time.
    SECS_BEFORE_LEAVE = 60
    # 1/n chance of ordering.

    # Increased by one when a table wants to order.
    # Decreased by one when a table gets their order.
    _num_waiting = 0

    INCREASE_FACTOR = 4
    MIN_DECIDING_SECS = 1
    MAX_DECIDING_SECS = 8
    _deciding_table = None
    _deciding_duration = 0
    _deciding_start = 0

    def __init__(
        self,
        kind,
        rect,
    ):
        super().__init__(kind, rect)
        # Needed to access instances.
        Table._tables.append(self)

        # A randomly chosen order. None if haven't ordered yet or just received food.
        self._order = None
        self._is_waiting = False
        self._order_start = 0

    def update(self, elapsed, *args, **kwargs):
        self._elapsed = elapsed
        # Only tables who haven't ordered can decide.
        choices = [table for table in self._tables if not table._order]

        # No deciding table yet.
        if not Table._deciding_table:
            # Choose a deciding table and begin random time to decide.
            Table._begin_deciding(choices, self._elapsed)
        # It is now time to order.
        if self._is_ready_to_order():
            # Get the right table and make it decide.
            Table._deciding_table._decide_order()

    def interact(self, player):
        """When player interacts, if order is ready, give player the
        order name.
        """
        # No order decided yet.
        if not self._has_order():
            return
        if not self._is_waiting:
            self._is_waiting = True
            player.take_order(self._order)
            return
        if player.ticket.is_done() and self._order == player.ticket.dish_name:
            player.give_dish()

    def _has_order(self) -> bool:
        """An order is available."""
        return self._order is not None

    def tell_order(self) -> str:
        """Return the randomly decided dish. Unshow popup."""
        # There is no longer a table actively deciding.
        self.unshow_interaction_popup()
        # Will return 'falsy' if order is not decided.
        return self._order

    def receive_dish(self) -> None:
        """Handles logic for a table getting a dish."""
        # Remove the sprite from the game.
        self._order = None
        Table._num_waiting -= 1

    @classmethod
    def _begin_deciding(cls, choices, elapsed) -> None:
        cls._deciding_table = random.choice(choices)
        cls._deciding_start = elapsed
        cls._set_deciding_duration()

    @classmethod
    def _set_deciding_duration(cls) -> None:
        cls._deciding_duration = random.uniform(
            (cls.MIN_DECIDING_SECS + (cls._num_waiting * cls.INCREASE_FACTOR)) * 1000,
            (cls.MAX_DECIDING_SECS + (cls._num_waiting * cls.INCREASE_FACTOR)) * 1000,
        )

    @classmethod
    def _unset_deciding_table(cls) -> None:
        cls._deciding_table = None

    def _decide_order(self) -> None:
        """Choose an item to order and call for the chef."""
        # I think I'll have a...
        self._order = random.choice(list(MENU.keys()))
        # Mark point in time when order took place.
        self._order_start = self._elapsed
        # Show popup.
        self.show_interaction_popup()

        Table._num_waiting += 1

        # No longer deciding
        self._unset_deciding_table()

    def _is_ready_to_order(self) -> bool:
        since = self._elapsed - Table._deciding_start
        return since > Table._deciding_duration
