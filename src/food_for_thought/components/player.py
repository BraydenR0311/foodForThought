import time
from typing import Protocol

import pygame as pg


from .. import config
from .ticket import Ticket
from .tile import InteractTile
from .generic import Generic
from .. import groups


class Player(pg.sprite.Sprite):
    IMAGE_PATHS = {
        "up_idle": config.IMAGE_DIR / "chef" / "up_idle.png",
        "up_walk_1": config.IMAGE_DIR / "chef" / "up_walk_1.png",
        "up_walk_2": config.IMAGE_DIR / "chef" / "up_walk_2.png",
        "right_idle": config.IMAGE_DIR / "chef" / "right_idle.png",
        "right_walk_1": config.IMAGE_DIR / "chef" / "right_walk_1.png",
        "right_walk_2": config.IMAGE_DIR / "chef" / "right_walk_2.png",
        "down_idle": config.IMAGE_DIR / "chef" / "down_idle.png",
        "down_walk_1": config.IMAGE_DIR / "chef" / "down_walk_1.png",
        "down_walk_2": config.IMAGE_DIR / "chef" / "down_walk_2.png",
        "left_idle": config.IMAGE_DIR / "chef" / "left_idle.png",
        "left_walk_1": config.IMAGE_DIR / "chef" / "left_walk_1.png",
        "left_walk_2": config.IMAGE_DIR / "chef" / "left_walk_2.png",
        "plate": config.IMAGE_DIR / "chef" / "plate.png",
    }

    images = {}

    containers = None

    ANIM_SPEED = 0.2
    SPEED = 150
    SPRINT_MULTIPLIER = 2

    def __init__(self, center):
        super().__init__(self.containers)
        self.index = 0
        self.dx = 0
        self.dy = 0
        self.image = self.images["up_idle"]
        self.rect = self.image.get_rect(center=center)
        self.time = time.time()
        self.center = pg.math.Vector2(0, 0)
        self._ticket = None
        self.plate = Generic(config.IMAGE_DIR / "chef" / "plate.png")
        self.plate.kill()

        self.animations = {
            "walk_up": [
                self.images["up_walk_1"],
                self.images["up_idle"],
                self.images["up_walk_2"],
                self.images["up_idle"],
            ],
            "walk_right": [
                self.images["right_walk_1"],
                self.images["right_idle"],
                self.images["right_walk_2"],
                self.images["right_idle"],
            ],
            "walk_down": [
                self.images["down_walk_1"],
                self.images["down_idle"],
                self.images["down_walk_2"],
                self.images["down_idle"],
            ],
            "walk_left": [
                self.images["left_walk_1"],
                self.images["left_idle"],
                self.images["left_walk_2"],
                self.images["left_idle"],
            ],
        }

    def update(self, dt, *args, **kwargs):
        self.center = pg.math.Vector2(*self.rect.center)

        self.plate.rect.bottomleft = self.rect.move(-15, 15).topright

        # # TODO: show plate
        # if (
        #     self._ticket is not None
        #     and self._ticket.is_done()
        #     and not self.plate.alive()
        # ):
        #     self.plate.add(self.plate.containers)
        # else:
        #     if self.plate.alive():
        #         self.plate.kill()

    def _hold_plate(self):
        if not self.plate.alive():
            self.plate.add(self.plate.containers)

    def _unhold_plate(self):
        if self.plate.alive():
            self.plate.kill()

    def interact(self, interact_tile) -> None:
        """Interact with an interactable tile."""
        interact_tile.interact(self)

    def take_order(self, dish_name: str):
        """Instantiate ticket with a given dish name string. Called by table."""
        # Player already has order
        if self.has_order():
            return
        self._ticket = Ticket(dish_name)
        self._hold_plate()

    def give_dish(self):
        """Give dish to table. Called by table."""
        self._ticket.kill()
        self._ticket = None
        self._unhold_plate()

    def has_order(self) -> bool:
        return self._ticket is not None

    def get_ticket(self) -> Ticket | None:
        return self._ticket

    def get_order_name(self) -> str | None:
        if not self.has_order():
            return
        return self.get_ticket().dish_name

    def in_range(self, interact_tile: InteractTile) -> bool:
        return self.rect.colliderect(interact_tile.get_interaction_rect())

    # def interact_table(self, table: Table) -> None:
    #     if table.has_order() and self._ticket is None:
    #         self._take_order(table)
    #     elif (
    #         self._ticket is not None
    #         and self._ticket.belongs_to(table)
    #         and self._ticket.is_done()
    #     ):
    #         self._give_dish(table)

    # def interact_appliance(self, appliance: Appliance) -> None:
    #     if not self._ticket:
    #         return (None, None)
    #     for ingr in self._ticket.get_unfinished():
    #         if appliance.can_cook(ingr.get_kind()):
    #             quote = self._ticket.quote.get()
    #             return (ingr, quote)
    #     return (None, None)

    def _give_dish(self, table: Table):
        """Give the dish to the table."""
        table.receive_dish()
        self._ticket.kill()
        self._ticket = None

    def get_distance_from(self, other: pg.sprite.Sprite):
        """Uses pygame's Vector2 to calculate Euclidean distance."""
        return self.center.distance_to(other.center)

    def animate(self, anim):
        self.elapsed = time.time() - self.time
        if self.elapsed > self.ANIM_SPEED:
            self.index = (self.index + 1) % len(anim)
            self.image = anim[self.index]
            self.time = time.time()
