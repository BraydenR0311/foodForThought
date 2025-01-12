import random

import pygame as pg

from paths import *
from src.components.food import Food
from src.components.tile import Tile
from src.components.text import Quote, Text
from src.components.generic import Generic

class Ticket(pg.sprite.Sprite):

    IMAGE_PATHS = {'ticket': IMAGE_DIR / 'ticket.png'}

    containers = None
    images = {}

    def __init__(self, dish_name):
        super().__init__(self.containers)
        # Quote to type out. Author for ticket title.
        # Initialized by ticket manager.
        self.quotes = None # Quote objects from quote split in 3.
        self.author_id = None # Unique id for author.
        self.author = None
        self.lastname = None
        self.author_face = None # Image of author's face.

        # Offsets for positioning
        self.first_offset = 20
        self.offset = 10 # Distance from edge of screen and other tickets.
        self.suboffset = 10 # Offset for attributes (ingredient, appliance hint, etc.)
        
        self.image = self.images['ticket']
        self.rect = self.image.get_rect()

        self.dish_name = dish_name
        # Text object that is used on the ticket.
        self.dishname_text = None
        self.ingredients = self._get_ingredients(Food.get_menu())

        # Keep track out which ingredients are finished.
        self.cooked = []
        
    def update(self, *args, **kwargs):
        # If all ingredients have been cooked.
        if len(self.cooked) >= 3:
            self.dishname_text.kill()
            for ingredient in self.cooked:
                ingredient.status.kill()
                ingredient.appliance_hint.kill()
                ingredient.kill()
            self.kill()

    
    def set_quote_data(self, quotes) -> None:
        """Used by TickeManager to get data."""
        # Generate random quote from quote data.
        quote_data = random.choice(quotes)
        # Extract data.
        quote = quote_data['quote']
        author_id = quote_data['id']
        author = quote_data['author']
        lastname = author.split(' ')[-1]
        
        quote = quote.replace('\n', ' ')
        quotes = self._split_quote(quote)
        quotes = [
            Quote(quote, ASSET_DIR / 'fonts' / 'pixel.ttf',15, 'black')
            for quote in quotes
        ]
        
        self.quotes = quotes
        self.author_id = author_id
        self.author = author
        self.lastname = lastname
        self.author_face = Generic(
            pg.image.load(
                IMAGE_DIR / 'faces' /(author_id + '.jpg')
            ).convert_alpha()
        )
        self.author_face.kill()
        # Now that we have the author, create the dishname Text object.
        self.dish_name_text = Text(
                ' '.join([self.lastname, self.dish_name]),
                ASSET_DIR / 'fonts' / 'pixel.ttf', 7, 'black'
        )

    def _get_ingredients(self, menu):
        return [Food(ingredient, Tile.get_images()) for ingredient in menu[self.dish_name]]

    @staticmethod
    def _split_quote(quote):
        quote = quote.split()
        chunk_len = len(quote) // 3

        first = ' '.join(quote[:chunk_len])
        second = ' '.join(quote[chunk_len:2 * chunk_len])
        third = ' '.join(quote[2 * chunk_len:])

        quotes = [first, second, third]

        return quotes
    

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
        self.spawning = False

        # Objects to be updated through the main loop.
        self.group = None
        self.shiftclock = None

    def update(self, ticket_group: pg.sprite.Group, time_elapsed):
        self.group = ticket_group
        self.time_elapsed = time_elapsed
        
        self.spawn_tickets()
        self.manage_locations()

    def spawn_tickets(self):
        # If not currently spawning and secs / spawn rate == 0.
        secs = self.time_elapsed // 1000
        if (not self.spawning and
            not secs % self.spawnrate and
            len(self.group) < self.max_tickets):
                dish_name = random.choice(Food.get_dish_names())
                ticket = Ticket(dish_name)
                ticket.set_quote_data(self.quotes)
                self.spawning = True
        elif (self.spawning and
              secs % self.spawnrate):
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
                        ticket.suboffset + ticket.first_offset
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
            # Position the dish name.
            #TODO: Turn this into a ticket attribute
            
            ticket.dish_name_text.rect.bottomleft = ticket.rect.bottomleft
            ticket.dish_name_text.rect.move_ip(ticket.suboffset, -ticket.suboffset)