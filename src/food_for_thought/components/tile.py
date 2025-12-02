from abc import ABC

import pygame as pg


from ..managers.gamestatemanager import GameStateManager
from ..managers.audiomanager import AudioManager
from .popup import Popup
from enum import Enum
from .. import config
from ..utils.image import Image, ImageCollection
from .. import groups

gamestate_manager = GameStateManager()
audio_manager = AudioManager()


class TileType(Enum):
    oven = "o"
    cutting_board = "c"
    fryer = "f"
    table = "t"
    floor = "#"
    player = "p"


# Only inherited from.
class Tile(pg.sprite.Sprite, ABC):
    tile_type_to_image_name = {
        TileType.floor: "floor",
        TileType.fryer: "fryer",
        TileType.oven: "oven",
        TileType.cutting_board: "cutting",
        TileType.table: "table",
    }

    containers = []
    images = ImageCollection(
        Image(config.TILE_DIR / "floor.png"),
        Image(config.TILE_DIR / "fryer.png"),
        Image(config.TILE_DIR / "oven.png"),
        Image(config.TILE_DIR / "cutting.png"),
        Image(config.TILE_DIR / "table.png"),
    )

    def __init__(self, tile_type: TileType, rect: pg.Rect):
        super().__init__()
        self.tile_type = tile_type
        self.image = self.images.get_surface(self.tile_type_to_image_name[tile_type])
        # Will overwrite this rect immediately.
        self.rect = rect
        if not self.containers:
            raise ValueError("Must define groups for this class.")
        self.add(*self.containers)


class Floor(Tile):
    containers = (groups.kitchen, groups.all_sprites)

    def __init__(self, tile_type: TileType, rect: pg.Rect):
        super().__init__(tile_type, rect)


class InteractTile(Tile):
    containers = (groups.interact_tiles, groups.kitchen, groups.all_sprites)

    def __init__(
        self,
        tile_type: TileType,
        rect: pg.Rect,
    ):
        super().__init__(tile_type, rect)
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
