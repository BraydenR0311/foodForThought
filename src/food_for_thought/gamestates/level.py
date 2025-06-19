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
from ..managers.tablemanager import TableManager


class Level(GameState):
    def __init__(self, statekey):
        super().__init__(statekey)

    @override
    def _setup(self):
        self.kitchen_rect = read_tilemap(
            config.ASSET_DIR / "map.txt", Player, Floor, Appliance, Table
        )
        self.tablemanager = TableManager(groups.tables)
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
            groups.appliances,
            key=lambda appliance: player.get_distance_from(appliance),
        )
        # Player is giving taking order or giving a dish to the table.
        if (
            # Within range of table.
            player.rect.colliderect(closest.get_hitbox())
            and
            # Interaction key is pressed.
            keys[pg.K_e]
        ):
            # Closest appliance is a table and is ready to order.
            if closest in groups.tables and closest.order:
                player.take_order(closest)
            # Closest appliance is a kitchen appliance.
            elif closest not in groups.tables:
                # Player has already taken an order.
                if player.ticket:
                    # Get quote sections in order.
                    quote = player.ticket.quote_sections[0]
                    for ingr in player.ticket.ingredients:
                        if closest.kind == ingr.APPLIANCE_DICT[ingr.kind]:
                            to_cook = ingr
                            self._gsmanager.goto(
                                StateKey.COOK, data={"to_cook": to_cook, "quote": quote}
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

        self.tablemanager.update(self.shiftclock.get_elapsed())

    @override
    def _draw(self):
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
