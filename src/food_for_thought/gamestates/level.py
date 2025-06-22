from typing import override

import pygame as pg

from .. import config
from .. import groups
from ..utils.utils import read_tilemap
from .gamestate import GameState
from .statekey import StateKey

from ..components.player import Player
from ..components.tile import Floor, Appliance, Table
from ..components.shiftclock import ShiftClock


class Level(GameState):
    def __init__(self, statekey):
        super().__init__(statekey)

    @override
    def _setup(self):
        self.kitchen_rect = read_tilemap(
            config.ASSET_DIR / "map.txt", Player, Floor, Appliance, Table
        )
        self.shiftclock = ShiftClock()
        self.pressing_e = False
        self.player = groups.player_group.sprite

    @override
    def enter(self):
        self.shiftclock.start()

    @override
    def exit(self):
        self.shiftclock.pause()

    @override
    def run(self):
        keys = pg.key.get_pressed()
        player = self.player

        # Directional Keybindings
        up = keys[pg.K_w]
        down = keys[pg.K_s]
        left = keys[pg.K_a]
        right = keys[pg.K_d]

        if up:
            player.dy = -player.speed
            player.animate(player.animations["walk_up"])
            player.rect.move_ip(0, player.dy)
        if down:
            player.dy = player.speed
            player.animate(player.animations["walk_down"])
            player.rect.move_ip(0, player.dy)
        hitlist = pg.sprite.spritecollide(player, groups.appliances, dokill=False)
        for sprite in hitlist:
            if player.dy > 0:
                player.rect.bottom = sprite.rect.top
            elif player.dy < 0:
                player.rect.top = sprite.rect.bottom
        if left:
            player.dx = -player.speed
            player.animate(player.animations["walk_left"])
            player.rect.move_ip(player.dx, 0)
        if right:
            player.dx = player.speed
            player.animate(player.animations["walk_right"])
            player.rect.move_ip(player.dx, 0)
        hitlist = pg.sprite.spritecollide(player, groups.appliances, dokill=False)
        for sprite in hitlist:
            if player.dx > 0:
                player.rect.right = sprite.rect.left
            elif player.dx < 0:
                player.rect.left = sprite.rect.right

        # Keep chef in the kitchen
        player.rect.clamp_ip(self.kitchen_rect)

        # Only interact with the closest appliance.
        closest = min(
            groups.interact_tiles,
            key=lambda appliance: player.get_distance_from(appliance),
        )

        # Within range of appliance and interaction key pressed.
        if player.rect.colliderect(closest.get_hitbox()) and keys[pg.K_e]:
            # Closest is ready to order
            if closest in groups.tables:
                player.take_order(closest)
            # Closest appliance is a kitchen appliance.
            elif closest not in groups.tables:
                # Player has already taken an order.
                if player.ticket:
                    for ingr in player.ticket.get_ingredients():
                        if closest.kind == ingr.APPLIANCE_DICT[ingr.get_kind()]:
                            # Pop a quote part from the quote.
                            quote = player.ticket.quote.get()
                            to_cook = ingr
                            self._gsmanager.goto(
                                StateKey.COOK,
                                data={
                                    "ticket": player.ticket,
                                    "to_cook": to_cook,
                                    "quote": quote,
                                    "shiftclock": self.shiftclock,
                                },
                            )

        self._update(closest=closest)
        self._draw()

    @override
    def _update(self, closest):
        groups.all_sprites.update(
            closest=closest,
            elapsed=self.shiftclock.get_elapsed(),
            player_rect=self.player.rect,
            keys=pg.key.get_pressed(),
        )

    @override
    def _draw(self):
        self._visualmanager.draw_background()
        self._visualmanager.draw(
            groups.kitchen,
            groups.player_group,
            groups.tickets,
            groups.foods,
            groups.statuses,
            groups.generics,
            groups.popups,
            groups.texts,
        )

    def _teardown(self):
        for sprite in groups.all_sprites:
            sprite.kill()
