from typing import override

import pygame as pg

from .. import config
from .. import groups
from .gamestate import GameState
from .statekey import StateKey

from ..components.player import Player
from ..components.tile import Floor, TileType
from ..components.appliance import Appliance

from ..components.table import Table
from ..components.levelclock import LevelClock
from ..managers.gamestatemanager import GameStateManager
from ..managers.visualmanager import VisualManager
from ..managers.audiomanager import AudioManager
from ..managers.tablemanager import TableManager
from .. import game_events
from pathlib import Path


import logging

logger = logging.getLogger(__name__)


gamestate_manager = GameStateManager()
visual_manager = VisualManager()
audio_manager = AudioManager()
table_manager = TableManager()


def read_tilemap(fp: Path) -> pg.Rect:
    with open(fp, "r", encoding="utf-8") as infile:
        tilemap = infile.read().splitlines()

    gridwidth = len(tilemap[0])
    if gridwidth % 2 == 0:  # Grid has even number of tiles.
        topleftx = visual_manager.get_screen_rect().centerx - (
            gridwidth // 2 * config.TILESIZE
        )
        toplefty = (
            visual_manager.get_screen_rect().centery
            - (gridwidth // 2 * config.TILESIZE),
        )
    else:  # Grid has odd number of tiles.
        topleftx = (
            visual_manager.get_screen_rect().centerx
            - (gridwidth // 2 * config.TILESIZE)
            - (config.TILESIZE // 2)
        )
        toplefty = (
            visual_manager.get_screen_rect().centery
            - (gridwidth // 2 * config.TILESIZE)
            - (config.TILESIZE // 2)
        )

    for i, row in enumerate(tilemap):
        for j, tile in enumerate(row):
            rect = pg.Rect(
                topleftx + j * config.TILESIZE,
                toplefty + i * config.TILESIZE,
                config.TILESIZE,
                config.TILESIZE,
            )

            match tile:
                case TileType.floor.value:
                    Floor(TileType.floor, rect)
                case TileType.player.value:
                    Floor(TileType.floor, rect)
                    Player(rect.center)
                case TileType.table.value:
                    Table(TileType.table, rect)
                case TileType.oven.value:
                    Appliance(TileType.oven, rect)
                case TileType.cutting_board.value:
                    Appliance(TileType.cutting_board, rect)
                case TileType.fryer.value:
                    Appliance(TileType.fryer, rect)
                case _:
                    logger.error("Unknown TileType: '%s'", tile)

    kitchen_rect = pg.Rect(
        topleftx, toplefty, gridwidth * config.TILESIZE, gridwidth * config.TILESIZE
    )

    return kitchen_rect


class Level(GameState):
    def __init__(self):
        super().__init__(StateKey.LEVEL)

    @override
    def _setup(self):
        self.kitchen_rect = read_tilemap(
            config.ASSET_DIR / "map.txt",
        )
        self.level_clock = LevelClock()
        self.player: Player = groups.player_group.sprite

    @override
    def _enter(self):
        self.level_clock.start()

    @override
    def _exit(self):
        self.level_clock.pause()

    @override
    def run(self):
        events = self.data["events"]
        dt = self.data["dt"]

        e_press = False
        for event in events:
            if event.type == pg.KEYDOWN and event.key == pg.K_e:
                e_press = True
            elif event.type == game_events.TABLE_RECEIVE_DISH:
                pass
            elif event.type == game_events.APPLIANCE_COOK:
                logger.debug(
                    "Cooking %s (%s) on %s",
                    event.cook_ingredient.metadata.name,
                    event.cook_ingredient.metadata.appliance,
                    event.appliance.tile_type,
                )
                gamestate_manager.goto(
                    StateKey.COOK,
                    data={
                        "ticket": event.ticket,
                        "appliance": event.appliance,
                        "level_clock": self.level_clock,
                        "cook_ingredient": event.cook_ingredient,
                    },
                )
            elif event.type == game_events.TABLE_RECEIVE_DISH:
                logger.debug("Dish received.")

        keys = pg.key.get_pressed()
        player = self.player

        # Directional Keybindings
        up = keys[pg.K_w]
        down = keys[pg.K_s]
        left = keys[pg.K_a]
        right = keys[pg.K_d]
        sprint = keys[pg.K_LSHIFT]

        if up:
            player.move("up", dt, sprint)
        if down:
            player.move("down", dt, sprint)

        collided_tiles = pg.sprite.spritecollide(
            player, groups.interact_tiles, dokill=False
        )
        for tile in collided_tiles:
            if player.dy > 0:
                player.rect.bottom = tile.rect.top
            elif player.dy < 0:
                player.rect.top = tile.rect.bottom
        if left:
            player.move("left", dt, sprint)
        if right:
            player.move("right", dt, sprint)
        collided_tiles = pg.sprite.spritecollide(
            player, groups.interact_tiles, dokill=False
        )
        for tile in collided_tiles:
            if player.dx > 0:
                player.rect.right = tile.rect.left
            elif player.dx < 0:
                player.rect.left = tile.rect.right

        # Keep chef in the kitchen
        player.rect.clamp_ip(self.kitchen_rect)

        # Only interact with the closest appliance.
        closest_interact_tile = min(
            groups.interact_tiles,
            key=lambda tile: player.get_distance_from(tile),
        )

        # Within range of appliance and interaction key pressed.
        if player.in_range(closest_interact_tile) and e_press:
            player.interact(closest_interact_tile)

        self._update()
        self._draw()

    @override
    def _update(self):
        groups.all_sprites.update(self.level_clock.get_elapsed(), self.data["dt"])
        table_manager.update(self.level_clock.get_elapsed())

    @override
    def _draw(self):
        visual_manager.draw_background()
        visual_manager.draw(
            groups.kitchen,
            groups.player_group,
            groups.tickets,
            groups.foods,
            groups.statuses,
            groups.generics,
            groups.popups,
            groups.texts,
        )

    @override
    def _teardown(self):
        for sprite in groups.all_sprites:
            sprite.kill()
