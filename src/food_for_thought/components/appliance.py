import pygame as pg

from .tile import InteractTile
import logging
from .. import game_events
from .player import Player
from .. import groups

logger = logging.getLogger(__name__)


class Appliance(InteractTile):
    containers = (
        groups.appliances,
        groups.interact_tiles,
        groups.kitchen,
        groups.all_sprites,
    )

    def __init__(
        self,
        tile_type,
        rect: pg.Rect,
    ):
        super().__init__(tile_type, rect)

    def interact(self, player: Player):
        ticket = player.get_ticket()
        if not ticket:
            return

        if not (cook_ingredient := ticket.get_cookable()):
            return

        if not cook_ingredient.metadata.appliance == self.tile_type:
            return

        pg.event.post(
            pg.event.Event(
                game_events.APPLIANCE_COOK,
                {
                    "appliance": self,
                    "ticket": ticket,
                    "cook_ingredient": cook_ingredient,
                },
            )
        )
