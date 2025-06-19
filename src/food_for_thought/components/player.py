import time

import pygame as pg

from .. import config
from .ticket import Ticket
from .tile import Table


# TODO: change time to pg ticks
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
    }

    images = {}

    containers = None

    ANIM_SPEED = 0.2

    def __init__(self, center):
        super().__init__(self.containers)
        self.index = 0
        self.speed = 2
        self.dx = 0
        self.dy = 0
        self.image = self.images["up_idle"]
        self.rect = self.image.get_rect(center=center)
        self.time = time.time()
        self.center = pg.math.Vector2(0, 0)
        self.ticket = None

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

    def update(self, closest, keys, *args, **kwargs):
        # TODO: Move this to main game loop
        self.center = pg.math.Vector2(*self.rect.center)

    def take_order(self, table: Table) -> None:
        """Receives order from a table if not already busy with another."""
        if not self.ticket:
            self.ticket = Ticket(table.tell_order())

    def give_dish(self, table: Table):
        """Give the dish to the table."""
        table.receive_dish()
        self.ticket.kill()

    def get_distance_from(self, other: pg.sprite.Sprite):
        """Uses pygame's Vector2 to calculate Euclidean distance."""
        return self.center.distance_to(other.center)

    def animate(self, anim):
        self.elapsed = time.time() - self.time
        if self.elapsed > self.ANIM_SPEED:
            self.index = (self.index + 1) % len(anim)
            self.image = anim[self.index]
            self.time = time.time()
