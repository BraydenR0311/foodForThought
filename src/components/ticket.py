import random

import pygame as pg

from paths import *
from src.common import MENU, QUOTE_DATA
from src.components.food import Food
from src.components.generic import Generic
from src.components.text import QuoteSection, Text
from src.utils.utils import get_screen_rect


class Ticket(pg.sprite.Sprite):
    """Manages QuoteSection and Food objects."""

    # First element(s) from top will be pushed down 30px.
    FIRST_OFFSET = 30
    # Offset for the rest of the elements displayed on the ticket.
    SUBOFFSET = 10

    IMAGE_PATHS = {"ticket": IMAGE_DIR / "ticket.png"}

    containers = None
    images = {}

    def __init__(self, dish_name):
        super().__init__(self.containers)
        self.image = self.images["ticket"]
        self.rect = self.image.get_rect()

        # Quote split into 'n' chunks as QuoteSection objects.
        self.quote_sections = []
        # Face image of whoever the quote is attributed to.
        self.author_image = None
        # Full name/title of the author.
        self.author = None
        # Only the lastname of the author.
        self.lastname = None

        self.dish_name = dish_name
        # Text object that is used on the ticket.
        self.dish_name_text = None
        self.ingredients = self._get_ingredients()

        # Now set all of of the data above.
        self._set_quote_data()
        # Position self and items.
        self._position_items()
        
        
    def update(self, *args, **kwargs):
        # Values will be True or False if quote is completed. Not None.
        if all(
            quote_sec.is_final_correct is not None
            for quote_sec in self.quote_sections
        ):
            self._finish()
            
    def get_score(self):
        """Retuns count of how many food items were cooked correctly."""
        return sum(quote.is_final_correct for quote in self.quote_sections)

    def _set_quote_data(self) -> None:
        """Choose a random quote and parse though its data to set values
        for this ticket."""
        # Get random quote from quote data.
        quote_data = random.choice(QUOTE_DATA)
        # Extract data.        
        self._set_author_image(quote_data['id'])
        self.author = quote_data['author']
        self.lastname = self.author.split(' ')[-1]
        
        # Generate QuoteSection objects.
        quote = quote_data['quote']
        # Fix any unwanted newlines.
        quote = quote.replace('\n', ' ')
        # Split text into 3 roughly even chunks.
        quote_sections = self._split_quote(quote)
        # Create quote_section objects.
        self.quote_sections = [
            QuoteSection(quote, 15, 'black') for quote in quote_sections
        ]
        # Now that we have the author, create the dishname Text object.
        # ie. 'Descartes Burger.'
        self.dish_name_text = Text(
                ' '.join([self.lastname, self.dish_name]), 7, 'black'
        )

    def _get_ingredients(self) -> list[Food]:
        """Create Food objects based on the dish and its ingredients."""
        return [Food(ingredient) for ingredient in MENU[self.dish_name]]

    def _finish(self):
        """Player has finished all 3 quotes."""
        for ingredient in self.ingredients:
            ingredient.kill()
            ingredient.appliance_hint.kill()
            ingredient.status.kill()
        self.author_image.kill()
        self.kill()
    
    def _set_author_image(self, author_id) -> None:
        """Helper method to create the author's face image and position."""
        self.author_image = Generic(
            (IMAGE_DIR / 'faces' / author_id).with_suffix('.jpg')
        )
        # Position the image relative to the ticket.
        self.author_image.rect.midright = self.rect.midleft
        # Move a little to the left.
        self.rect.move_ip(-10, 0)

    def _position_items(self):
        """Position self and objects within self."""
        # Position self.
        self.rect.midtop = get_screen_rect().midtop
        self.rect.move_ip(0, self.SUBOFFSET)

        #Position ingredients.
        previous_ingredient = None
        for ingredient in self.ingredients:
            # Position first ingredient.
            if not previous_ingredient:
                # Match topleft corners.
                ingredient.rect.topleft = self.rect.topleft
                # Offset first ingredient.
                ingredient.rect.move_ip(self.SUBOFFSET, self.FIRST_OFFSET)
            else:
                # Match topleft corner to bottom left of previous ingredient.
                ingredient.rect.topleft = previous_ingredient.rect.bottomleft
                ingredient.rect.move_ip(0, self.SUBOFFSET)

            ingredient.appliance_hint.rect.midleft = ingredient.rect.midright
            ingredient.appliance_hint.rect.move_ip(self.SUBOFFSET, 0)

            previous_ingredient = ingredient

            self.dish_name_text.rect.bottomleft = self.rect.bottomleft
            self.dish_name_text.rect.move_ip(self.SUBOFFSET, -self.SUBOFFSET)

    def _undraw(self):
        """Use when initializing so elements are not drawn yet."""
        self.kill()
        self.dish_name_text.kill()
        for ingredient in self.ingredients:
            ingredient.kill()
            ingredient.appliance_hint.kill()
        
    def draw(self):
        self.add(self.containers)
        self.dish_name_text.add(self.containers)
        for ingredient in self.ingredients:
            ingredient.add(ingredient.containers)

    @staticmethod
    def _split_quote(quote):
        """Helper method to split the quote into even chunks."""
        quote = quote.split()
        chunk_len = len(quote) // 3

        first = ' '.join(quote[:chunk_len])
        second = ' '.join(quote[chunk_len:2 * chunk_len])
        third = ' '.join(quote[2 * chunk_len:])

        quotes = [first, second, third]

        return quotes
    
