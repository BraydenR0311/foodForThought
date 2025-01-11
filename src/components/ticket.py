import random

import pygame as pg

from paths import *
from src.utils.utils import quotegen
from src.components.food import Food
from src.components.text import Quote

class Ticket(pg.sprite.Sprite):

    containers = None

    def __init__(self, dishname):
        super().__init__(self.containers)
        # Quote to type out. Author for ticket title.
        # Initialized by ticket manager.
        self.author, self.quotes = None, None
        # Dimensions of ticket.
        self.size = (100, 150)

        # Offsets for positioning
        self.offset = 10 # Distance from edge of screen and other tickets.
        self.suboffset = 10 # Offset for attributes (ingredient, appliance hint, etc.)
        
        self.image = pg.Surface(self.size)
        self.rect = self.image.get_rect()

        self.dishname = dishname
        self.dish = Food(self.dishname)
        self.ingredients = self._get_ingredients(Food.DISH_DICT)

        self.cooked = []
        
    def update(self):
        self.image.fill('white')

        # If all ingredients have been cooked.
        if len(self.cooked) >= 3:
            self.dish.kill()
            for ingredient in self.cooked:
                ingredient.status.kill()
                ingredient.appliance_hint.kill()
                ingredient.kill()
            self.kill()

    def _get_ingredients(self, dish_ingr_map):
        return [Food(ingredient) for ingredient in dish_ingr_map[self.dishname]]
            
    def split_quote(quote):
        quote = quote.split()
        chunk_len = len(quote) // 3

        first = ' '.join(quote[:chunk_len])
        second = ' '.join(quote[chunk_len:2 * chunk_len])
        third = ' '.join(quote[2 * chunk_len:])

        quotes = [first, second, third]

        return quotes
    
    def set_quotes(self, quotes):
        author, quote = quotegen(quotes)
        quote = quote.split()
        chunk_len = len(quote) // 3

        first = ' '.join(quote[:chunk_len])
        second = ' '.join(quote[chunk_len:2 * chunk_len])
        third = ' '.join(quote[2 * chunk_len:])

        quotes = [first, second, third]
        quotes = [Quote(quote, ASSET_DIR / 'fonts' / 'pixel.ttf',
                        15, 'black') for quote in quotes]

        self.author, self.quotes = author, quotes
    
class TicketManager:
    def __init__(self, spawnrate: int, max_tickets: int, quotes):
        """Parameters:
        ---
            - spawnrate: seconds before next spawn.
            - group: ticket container.
            - max_tickets: max num of tickets on screen.
        """
        self.spawnrate = spawnrate
        self.max_tickets = max_tickets
        self.quotes = quotes
        self.choices = list(Food.DISH_DICT)
        self.spawning = False

        # Objects to be updated through the main loop.
        self.group = None
        self.shiftclock = None

    def update(self, ticket_group: pg.sprite.Group, shiftclock):
        self.group = ticket_group
        self.shiftclock = shiftclock
        
        self.spawn_tickets()
        self.manage_locations()

    def spawn_tickets(self):
        # If not currently spawning and secs / spawn rate == 0.
        if (not self.spawning and
            not self.shiftclock.secs % self.spawnrate and
            len(self.group) <= self.max_tickets):
                food = random.choice(self.choices)
                ticket = Ticket(food)
                ticket.set_quotes(self.quotes)
                self.spawning = True
        elif (self.spawning and
              self.shiftclock.secs % self.spawnrate):
            self.spawning = False

    def manage_locations(self):
        for i, ticket in enumerate(reversed(self.group.sprites())):
            # Position tickets.
            ticket.rect.topleft = (
                ticket.offset + i*(ticket.rect.width + ticket.offset),
                ticket.offset
            )
            # Position ingredients.
            previous_ingredient = None
            for ingredient in ticket.ingredients:
                if not previous_ingredient:
                    # Position ingredient icon.
                    ingredient.rect.topleft = ticket.rect.topleft
                    ingredient.rect.move_ip(
                        ticket.suboffset,
                        ticket.suboffset
                    )
                else:
                    # Position according to last ingredient
                    ingredient.rect.topleft = previous_ingredient.rect.bottomleft
                    ingredient.rect.move_ip(
                        0, # Already aligned.
                        ticket.suboffset
                    )
                previous_ingredient = ingredient
                # Position appliance hint.
                ingredient.appliance_hint.rect.midleft = ingredient.rect.midright
                ingredient.appliance_hint.rect.move_ip(
                    ticket.suboffset,
                    0 # Already aligned vertically.
                )
                # Position status
                ingredient.status.rect.midleft = ingredient.appliance_hint.rect.midright
                ingredient.status.rect.move_ip(
                    ticket.suboffset,
                    0
                )
            # Position the dish.
            ticket.dish.rect.bottomleft = ticket.rect.bottomleft
            ticket.dish.rect.move_ip(ticket.suboffset, -ticket.suboffset)
            # Position status.
            ticket.dish.status.rect.midleft = ticket.dish.rect.midright
            ticket.dish.status.rect.move_ip(ticket.suboffset, 0)