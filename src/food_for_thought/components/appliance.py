import pygame as pg

from .tile import InteractTile
import logging
from .. import game_events
from .player import Player

logger = logging.getLogger(__name__)


class Appliance(InteractTile):
    def __init__(
        self,
        tile_type,
        rect: pg.Rect,
    ):
        super().__init__(tile_type, rect)

    def interact(self, player):
        ticket = player.get_ticket()
        if not ticket:
            return
        pg.event.post(pg.event.Event(game_events.APPLIANCE_COOK, {"appliance": self}))
