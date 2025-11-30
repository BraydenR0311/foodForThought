import time

import pygame as pg


from .. import config
from .ticket import Ticket
from .tile import InteractTile, TileType
from .generic import Generic


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
    TILE_TYPE = TileType.player

    images = {}

    containers = None

    ANIM_SPEED = 0.2
    BASE_VELOCITY = 150
    SPRINT_MULTIPLIER = 2

    tile_type = TileType.player

    def __init__(self, center):
        super().__init__(self.containers)
        self.index = 0
        self.dx = 0
        self.dy = 0

        self.image = self.images["up_idle"]
        self.rect = self.image.get_rect(center=center)
        self.time = time.time()
        self.center = pg.math.Vector2(*self.rect.center)
        self._ticket = None
        self.plate = None

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
        self.center.xy = self.rect.center

        if self.plate:
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

    def move(self, direction: str, dt: float, sprint: bool) -> None:
        sprint_multiplier = Player.SPRINT_MULTIPLIER if sprint else 1
        match direction:
            case "up":
                self.dy = -Player.BASE_VELOCITY * dt * sprint_multiplier
                self.animate(self.animations["walk_up"])
                self.rect.move_ip(0, self.dy)
            case "down":
                self.dy = Player.BASE_VELOCITY * dt * sprint_multiplier
                self.animate(self.animations["walk_down"])
                self.rect.move_ip(0, self.dy)
            case "left":
                self.dx = -Player.BASE_VELOCITY * dt * sprint_multiplier
                self.animate(self.animations["walk_left"])
                self.rect.move_ip(self.dx, 0)
            case "right":
                self.dx = Player.BASE_VELOCITY * dt * sprint_multiplier
                self.animate(self.animations["walk_right"])
                self.rect.move_ip(self.dx, 0)

    def interact(self, interact_tile) -> None:
        """Interact with an interactable tile."""
        interact_tile.interact(self)

    def take_order(self, dish_name: str):
        """Instantiate ticket with a given dish name string. Called by table."""
        # Player already has a ticket.
        if self._ticket:
            return
        self._ticket = Ticket(dish_name)

    def has_ticket(self) -> bool:
        return self._ticket is not None

    def give_order(self):
        """Give dish to table. Called by table."""
        self._ticket.kill()
        self._ticket = None
        self._unhold_plate()

    def get_dish_name(self) -> str | None:
        if not self._ticket:
            return None
        return self._ticket.get_dish_name()

    def has_finished_order(self) -> bool:
        return not self._ticket or self._ticket.is_done()

    def _hold_plate(self):
        if not self.plate:
            self.plate = Generic(config.IMAGE_DIR / "chef" / "plate.png")

    def _unhold_plate(self):
        if self.plate:
            self.plate.kill()

    def get_ticket(self) -> Ticket | None:
        return self._ticket

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

    def get_distance_from(self, other: pg.sprite.Sprite):
        """Uses pygame's Vector2 to calculate Euclidean distance."""
        return self.center.distance_to(other.center)

    def animate(self, anim):
        self.elapsed = time.time() - self.time
        if self.elapsed > self.ANIM_SPEED:
            self.index = (self.index + 1) % len(anim)
            self.image = anim[self.index]
            self.time = time.time()
