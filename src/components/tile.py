from abc import ABC
import random

import pygame as pg

from paths import *
from src.config import Config
from src.components.popup import Popup
from src.components.ticket import Ticket
from src.shared_data import TILE_IMAGE_PATHS, MENU


# Only inherited from.
class Tile(ABC):
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
            raise ValueError('Must define groups for this class.')
        self.add(self.containers)

class Floor(Tile, pg.sprite.Sprite):
    def __init__(self, kind, rect):
        super().__init__(kind, rect)

class Appliance(Tile, pg.sprite.Sprite):
    def __init__(self, kind, rect):
        super().__init__(kind, rect)
        # Define the allowable area for player interaction.
        self.zone = self.rect.inflate(70, 70)
        self.popup = Popup(self.rect.center, 'e_hint')
        self.center = pg.math.Vector2(*self.rect.center)

    def update(self, player_rect, closest, *args, **kwargs):
        # Show interaction if player is closest and within range.
        if self is closest and self.zone.colliderect(player_rect):
            self._show_interact_popup()
        else:
            self._unshow_interact_popup()

    def get_hitbox(self) -> pg.Rect:
        '''Return the area where the user can interact.'''
        return self.zone

    def _show_interact_popup(self):
        self.popup.add(Popup.containers)
    
    def _unshow_interact_popup(self):
        self.popup.kill()


class Table(Appliance, pg.sprite.Sprite):
    # Minimum time until table can order again after receiving food or game starts.
    ORDER_COOLDOWN = 15
    # Will leave at this time.
    TIME_BEFORE_LEAVE = 60
    # 1/n chance of ordering.
    order_chance = 60

    # Increased by one when a table wants to order.
    # Decreased by one when a table gets their order.
    num_waiting = 0

    def __init__(self, kind, rect):
        super().__init__(kind, rect)
        # A popup that says 'waiter!'.
        self.popup = Popup(self.rect.center, 'order')
        # A randomly chosen order. None if haven't ordered yet or just received food.
        self.order = None

    def update(self, elapsed, *args, **kwargs):
        self.elapsed = elapsed


    def _decide_order(self) -> None:
        '''Choose an item to order and call for the chef.'''
        # I think I'll have a...
        self.order = random.choice(list(MENU.keys()))
        # Show popup.
        self.popup.add(Popup.containers)

    def tell_order(self) -> str:
        '''Return the randomly decided dish. Unshow popup.'''
        self.popup.kill()
        # Will return 'falsy' if order is not decided. 
        print(self.order) 
        return self.order
    
    def receive_dish(self) -> None:
        '''Handles logic for a table getting a dish.'''
        # Remove the sprite from the game.
        self.order = None


