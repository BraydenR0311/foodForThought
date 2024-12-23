from enum import Enum, auto

import pygame as pg

from src.config import Config
from utils.utils import quoteread
from paths import *

class State(Enum):
    MAIN_MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    TYPING = auto()

class GameManager:
    def __init__(self):
        self.screen = None
        self.clock = pg.time.Clock()
        self.quotes = quoteread(ASSET_DIR / 'quotes.txt')
        self.state = State.MAIN_MENU

    def load_screen(self):
        screen = pg.display.set_mode((Config.WIDTH, Config.HEIGHT))
        self.screen = screen

    def draw_background(self, background_image: pg.Surface):
        self.screen.blit(background_image)

    def draw(self, *groups):
        """
        Draws groups to the screen in order listed.
        """
        for group in groups:
            group.draw(self.screen)

    def get_quotes(self):
        return self.quotes
    
    def set_state(self, new_state):
        self.state = new_state