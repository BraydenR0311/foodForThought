import pygame as pg
import random
from ..common import MENU

from .tile import InteractTile


class Table(InteractTile):
    # Increased by one when a table wants to order.
    # Decreased by one when a table gets their order.
    _num_waiting = 0

    _deciding_table = None
    _deciding_duration = 0
    _deciding_start = 0

    def __init__(
        self,
        kind,
        rect,
    ):
        super().__init__(kind, rect)

        # A randomly chosen order. None if haven't ordered yet or just received food.
        self._decided_dish_name = ""
        self._is_waiting = False
        self._has_order_taken = False
        self._order_start = 0

    def update(self, elapsed, *args, **kwargs):
        pass

    def has_order_taken(self) -> bool:
        """Order has been taken by player. Table is waiting for food"""
        return self._has_order_taken

    def is_waiting(self) -> bool:
        """Table is waiting for food. Player may or may not be working on it"""
        return self._is_waiting

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
