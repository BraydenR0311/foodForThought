import string

import pygame as pg

from paths import *
from src.utils.utils import get_screen_rect

class Text(pg.sprite.Sprite):
    '''Simple text that can be rendered and acts like a sprite.'''
    containers = None

    def __init__(self, text, fontsize, color, bgcolor=None):
        super().__init__(self.containers)
        self.text = str(text)
        self.font = pg.font.Font(FONT_DIR / 'pixel.ttf', fontsize)
        self.color = color
        self.bgcolor = bgcolor
        self.image = self.font.render(self.text, 1, self.color, self.bgcolor)
        self.rect = self.image.get_rect()


class QuoteSection(Text):
    '''Extended Text class that handles user input and typing logic.'''
    containers = None

    def __init__(self, text, fontsize, color, bgcolor=None):
        super().__init__(text, fontsize, color, bgcolor)
        # Initialize empty input. Will update with each keystroke.
        self.user_input = Text('', fontsize, 'green')
        # Position the quote in the right place (centered and below kitchen.)
        self.rect.center = get_screen_rect().center
        self.rect = self.rect.move(0, get_screen_rect().height // 3)
        # Put user input in the same place on the screen.
        self.user_input.rect = self.rect
        # Number of wrong inputs.
        self.misses = 0
        # Flag to prevent self.misses from going up 1 each frame.
        self.is_wrong = False
        # After typing is done, did user type it correctly?
        self.is_final_correct = None

    def update(self, *args, **kwargs):
        # User mistypes and needs to backspace to go continue typing.
        if not self.text.startswith(self.user_input.text) and not self.is_wrong:
            self._make_wrong()
        # User backspaces.
        elif self.text.startswith(self.user_input.text) and self.is_wrong:
            self._make_correction()        
            
        # User typed quote correctly.
        if self.user_input.text == self.text:
            self.finish_correctly()
        # User messes up for a 3rd time.     
        elif self.misses >= 3:
            self.finish_incorrectly()
        
        self._update_user_input()

    # Needs pg.event.get() as events
    def handle_input(self, events):
        for event in events:
            # User types something.
            if event.type == pg.TEXTINPUT:
                if (
                    # Text is ascii.
                    event.text in string.ascii_letters
                    + string.digits
                    + string.punctuation
                    +  ' ' and
                    # Prevent typing more if already wrong.
                    not self.is_wrong
                ):
                    # Add new character.
                    self.user_input.text = self.user_input.text + event.text
            elif (
                # If user pressed backspace.
                event.type == pg.KEYDOWN and
                event.key == pg.K_BACKSPACE
            ):
                # Remove a character.
                self.user_input.text = self.user_input.text[:-1]

    def get_final_result(self):
        '''True if quote section was correctly typed. False if not.'''
        return self.is_final_correct

    def finish_correctly(self):
        '''Logic for user correctly typing quote.'''
        # Remove sprites from the screen and clean up.
        self.user_input.kill() 
        self.kill()
        self.is_final_correct = True
            
    def finish_incorrectly(self):
        '''Logic for user incorrectly typing quote.'''
        self.user_input.kill()
        self.kill()

    def _make_wrong(self):
        '''User messes up and types an incorrect character.'''
        self.is_wrong = True
        self.user_input.color = 'red'
        self.misses += 1

    def _make_correction(self):
        '''Correct user after backspacing.'''
        self.is_wrong = False
        self.user_input.color = 'green'

    def _update_user_input(self):
        '''Must be called to update the color and letters of input text'''
        self.user_input.image = self.font.render(
            self.user_input.text, 1, self.user_input.color
        )
