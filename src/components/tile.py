from abc import ABC
import random

import pygame as pg

from paths import *
from src.config import Config
from src.components.status import Popup
from src.components.ticket import Ticket
from shared_data import TILE_IMAGE_PATHS, MENU


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
        if self.containers == None:
            raise ValueError('Must define groups for this class.')
        self.add(self.containers)

    @classmethod
    def get_images(cls) -> dict[str, pg.Surface]:
        return cls.images

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
        if self is closest and self.zone.colliderect(player_rect):
            print('closest', self.rect)
            self.popup.add(Popup.containers)
        else:
            self.popup.kill()

    def get_hitbox(self) -> pg.Rect:
        '''Return the area where the user can interact.'''
        return self.zone

class Table(Appliance, pg.sprite.Sprite):
    # Minimum time until table can order again after receiving food or game start.
    ORDER_COOLDOWN = 15
    # Max amount of time a table can decide what to order.
    MAX_COOLDOWN_TIME = 30
    # Will leave at this time.
    TIME_BEFORE_LEAVE = 60

    def __init__(self, kind, rect):
        super().__init__(kind, rect)
        # A popup that says 'waiter!'.
        self.popup = Popup(self.rect.center, 'order')
        # A randomly chosen order. None if haven't ordered yet or just received food.
        self.ticket = None
        # Table's awareness of time passed since round start.
        self.elapsed = 0
        # Marks the time that the order was taken. 0 if haven't ordered yet.
        self.time_of_order = None

    def update(self, elapsed, *args, **kwargs):
        self.elapsed = elapsed
        if self.elapsed > self.ORDER_COOLDOWN:
            self.decide_order()

    def decide_order(self):
        '''Choose an item to order and call for the chef.'''
        # Already chose an order.
        if self.ticket:
            return
        # Waiter, I'd like a...
        self.ticket = Ticket(random.choice(MENU))
        # Show popup.
        self.popup.add(Popup.containers)

    def get_order(self):
        '''Return the ticket object with the randomly decided dish.'''
        # An order has been decided.
        if self.ticket: 
            # Mark time when order was taken.
            self.time_of_order = self.elapsed 
        return self.ticket
    
    def get_time_since_order(self):
        '''Calculate how long since user interacted and received the order.'''
        # Order has not been taken yet.
        if not self.time_of_order:
            return None
        return self.elapsed - self.time_of_order
    
    def receive_dish(self):
        '''Handles logic for a table getting a dish.'''
        # Remove the sprite from the game.
        self.ticket.kill()
        self.ticket = None
        # Reset the time of order to None, since table hasn't ordered yet.
        self.time_of_order = None



    