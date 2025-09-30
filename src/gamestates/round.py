import pygame as pg
from config import *

from src import groups
from src.utils.utils import read_tilemap
from src.components.button import Button
from src.gamestates.gamestate import GameState
from src.gamestates.statekey import StateKey
from src.components.shiftclock import ShiftClock
from src.components.player import Player
from src.components.tile import Floor, Appliance, Table


class Round(GameState):
    def __init__(self, statekey):
        super().__init__(statekey)

        self.kitchen_rect = read_tilemap(
            ASSET_DIR / "map.txt", Player, Floor, Appliance, Table
        )
        self.tablemanager = TableManager(tables)
        self.player = groups.players.sprites()[0]
        self.shiftclock = ShiftClock()

    def update(self, keys, closest):
        groups.all_sprites.update(
            elapsed=self.shiftclock.get_elapsed(),
            player_rect=self.player.rect,
            keys=keys,
            closest=closest,
        )

        self.tablemanager.update(self.shiftclock.get_elapsed())

    def run(self):
        closest = min(
            groups.appliances,
            key=lambda appliance: self.player.get_distance_from(appliance),
        )
        keys = pg.key.get_pressed()

        self.update(keys, closest)

        # Directional Keybindings
        up = keys[pg.K_w]
        down = keys[pg.K_s]
        left = keys[pg.K_a]
        right = keys[pg.K_d]

        if up:
            self.player.dy = -self.player.speed
            self.player.animate(self.player.animations["walk_up"])
            self.player.rect.move_ip(0, self.player.dy)
        if down:
            self.player.dy = self.player.speed
            self.player.animate(self.player.animations["walk_down"])
            self.player.rect.move_ip(0, self.player.dy)
        hitlist = pg.sprite.spritecollide(self.player, groups.appliances, False)
        for sprite in hitlist:
            if self.player.dy > 0:
                self.player.rect.bottom = sprite.rect.top
            elif self.player.dy < 0:
                self.player.rect.top = sprite.rect.bottom
        if left:
            self.player.dx = -self.player.speed
            self.player.animate(self.player.animations["walk_left"])
            self.player.rect.move_ip(self.player.dx, 0)
        if right:
            self.player.dx = self.player.speed
            self.player.animate(self.player.animations["walk_right"])
            self.player.rect.move_ip(self.player.dx, 0)
        hitlist = pg.sprite.spritecollide(self.player, groups.appliances, False)
        for sprite in hitlist:
            if self.player.dx > 0:
                self.player.rect.right = sprite.rect.left
            elif self.player.dx < 0:
                self.player.rect.left = sprite.rect.right

        self.player.rect.clamp_ip(self.kitchen_rect)
        # Player is giving taking order or giving a dish to the table.
        if (
            # Within range of table.
            self.player.rect.colliderect(closest.get_hitbox())
            and
            # Interaction key is pressed.
            keys[pg.K_e]
        ):
            # Closest appliance is a table and is ready to order.
            if closest in groups.tables and closest.order:
                self.player.take_order(closest)
            # Closest appliance is a kitchen appliance.
            elif closest not in groups.tables:
                # Player has already taken an order.
                if self.player.ticket:
                    # Get quote sections in order.
                    quote = self.player.ticket.quote_sections[0]
                    for ingr in self.player.ticket.ingredients:
                        if closest.kind == ingr.APPLIANCE_DICT[ingr.kind]:
                            ingredient_to_cook = ingr
                            self.gsmanager.goto(StateKey.TYPING)

    def draw(self):
        screen = self.visualmanager.get_screen()
        draw_groups = [
            groups.kitchen,
            groups.players,
            groups.tickets,
            groups.foods,
            groups.statuses,
            groups.generics,
            groups.texts,
            groups.shiftclock_group,
            groups.popups,
        ]
        self.visualmanager.draw_background()
        for group in draw_groups:
            group.draw(screen)

    def cleanup(self):
        for sprite in all_sprites:
            sprite.kill()
