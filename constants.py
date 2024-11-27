import pygame as pg
from enum import Enum, auto

from paths import *
from src.services import quoteread

WIDTH = 1280
HEIGHT = 720
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
SCREEN_RECT = SCREEN.get_rect()
FPS = 60
# Tiles must all be the same pixel size.
TILESIZE = 75

QUOTES = quoteread(ASSET_DIR / 'quotes.txt')

class Gamestates(Enum):
    MAIN_MENU = auto()
    PLAYING = auto()
    PAUSED = auto()