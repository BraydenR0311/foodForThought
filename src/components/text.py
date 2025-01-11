import string

import pygame as pg

from paths import *
from src.utils.utils import get_screen_rect

class Text(pg.sprite.Sprite):

    containers = None

    def __init__(self, text, font, fontsize, color, bgcolor=None):
        super().__init__(self.containers)
        self.text = str(text)
        self.font = pg.font.Font(font, fontsize)
        self.color = color
        self.bgcolor = bgcolor
        self.image = self.font.render(self.text, 1, self.color, self.bgcolor)
        self.rect = self.image.get_rect()

class Quote(Text):

    containers = None

    def __init__(self, text, font, fontsize, color, bgcolor=None):
        super().__init__(text, font, fontsize, color, bgcolor)
        # User input used to color text.
        self.user = Text('', font, fontsize, 'green')
        self.rect.center = get_screen_rect().center
        self.rect = self.rect.move(0, get_screen_rect().height // 3)
        self.user.rect = self.rect
        self.wrongs = 0
        self.wronged = False
        self.is_correct = False

    def update(self):
        self.image = self.font.render(self.text, 1, self.color, self.bgcolor)
        
        if self.user.text == self.text:
            self.user.kill() # Kill user input.
            self.kill() # Kill original text.
            self.is_correct = True
        
        elif self.wrongs >= 3:
            self.user.kill()
            self.kill()

        if (not self.text.startswith(self.user.text) and
            not self.wronged):
            self.wronged = not self.wronged
            self.color = 'red'
            self.wrongs += 1
            
        elif self.text.startswith(self.user.text):
            if self.wronged:
                self.wronged = not self.wronged
            self.color = 'black'
            self.user.image = self.font.render(self.user.text, 1, self.user.color)

    # Needs pg.event.get() as events
    def handle_ipnut(self, events):
        for event in events:
            if event.type == pg.TEXTINPUT:
                if (event.text in string.ascii_letters
                    + string.digits
                    + string.punctuation
                    +  ' ' and
                    not self.wronged):
                    self.user.text = self.user.text + event.text
            elif (event.type == pg.KEYDOWN and
                  event.key == pg.K_BACKSPACE):
                    self.user.text = self.user.text[:-1]