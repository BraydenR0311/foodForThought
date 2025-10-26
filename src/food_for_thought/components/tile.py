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
