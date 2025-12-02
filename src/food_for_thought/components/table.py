import pygame as pg
import random


from .tile import InteractTile, TileType
from .menu import MENU
from .. import game_events
import logging
from .. import groups

logger = logging.getLogger(__name__)


class Table(InteractTile):
    containers = (
        groups.tables,
        groups.interact_tiles,
        groups.kitchen,
        groups.all_sprites,
    )
    # Increased by one when a table wants to order.
    # Decreased by one when a table gets their order.

    def __init__(
        self,
        tile_type: TileType,
        rect,
    ):
        super().__init__(tile_type, rect)

        # A randomly chosen order. None if haven't ordered yet or just received food.
        self._decided_dish_name = ""
        # Order has been taken. Still technically 'waiting'.
        self._order_taken = False
        self._order_start = 0
        self._popup = None

    def update(self, elapsed, *args, **kwargs):
        pass

    def interact(self, player):
        """When player interacts, if order is ready, give player the
        order name.
        """
        # No order decided yet.
        if not self._decided_dish_name:
            return

        # Player already has a ticket.
        if player.has_ticket():
            return
        # Has decided a dish. Player will take order now.
        if not self._order_taken:
            player.take_order(self._decided_dish_name)
            self._order_taken = True
            self.unshow_interaction_popup()
            return

        finished_ticket_dish_name = player.get_finished_dish_name()
        if not finished_ticket_dish_name:
            return
        if self._decided_dish_name == finished_ticket_dish_name:
            self._receive_order()

    def decide_order(self):
        if self._decided_dish_name:
            return
        self._decided_dish_name = random.choice(list(MENU.keys()))
        logger.debug("Decided dish: %s", self._decided_dish_name)
        self.show_interaction_popup()

    def can_order(self) -> bool:
        return not self._decided_dish_name

    def _receive_order(self):
        self._decided_dish_name = ""
        self._order_taken = False
        pg.event.post(pg.event.Event(game_events.TABLE_RECEIVE_DISH, {"table": self}))
