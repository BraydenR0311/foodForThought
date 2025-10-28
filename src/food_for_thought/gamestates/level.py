from typing import override

import pygame as pg

from .. import config
from .. import groups
from ..utils.utils import read_tilemap
from .gamestate import GameState
from .statekey import StateKey

from ..components.player import Player
from ..components.tile import Floor, Appliance
from ..components.table import Table
from ..components.levelclock import LevelClock
from ..managers.gamestatemanager import GameStateManager
from ..managers.visualmanager import VisualManager
from ..managers.audiomanager import AudioManager

gamestate_manager = GameStateManager()
visual_manager = VisualManager()
audio_manager = AudioManager()


class Level(GameState):
    def __init__(self):
        super().__init__(StateKey.LEVEL)

    @override
    def _setup(self):
        self.kitchen_rect = read_tilemap(
            config.ASSET_DIR / "map.txt",
            Player,
            Floor,
            Appliance,
            Table,
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

        keys = pg.key.get_pressed()
        player = self.player

        # Directional Keybindings
        up = keys[pg.K_w]
        down = keys[pg.K_s]
        left = keys[pg.K_a]
        right = keys[pg.K_d]
        sprint = keys[pg.K_LSHIFT]

        speed = player.SPEED
        if sprint:
            speed *= player.SPRINT_MULTIPLIER
        if up:
            player.dy = -speed * dt
            player.animate(player.animations["walk_up"])
            player.rect.move_ip(0, player.dy)
        if down:
            player.dy = speed * dt
            player.animate(player.animations["walk_down"])
            player.rect.move_ip(0, player.dy)
        collided_tiles = pg.sprite.spritecollide(
            player, groups.interact_tiles, dokill=False
        )
        for tile in collided_tiles:
            if player.dy > 0:
                player.rect.bottom = tile.rect.top
            elif player.dy < 0:
                player.rect.top = tile.rect.bottom
        if left:
            player.dx = -speed * dt
            player.animate(player.animations["walk_left"])
            player.rect.move_ip(player.dx, 0)
        if right:
            player.dx = speed * dt
            player.animate(player.animations["walk_right"])
            player.rect.move_ip(player.dx, 0)
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
        groups.all_sprites.update(
            elapsed=self.level_clock.get_elapsed(), dt=self.data["dt"]
        )

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
