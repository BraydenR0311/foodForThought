import pygame as pg
from enum import Enum, auto

WIDTH = 1280
HEIGHT = 720
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
SCREEN_RECT = SCREEN.get_rect()
# Tiles must all be the same pixel size.
TILESIZE = 75

class Gamestates(Enum):
    MAIN_MENU = auto()
    PLAYING = auto()
    PAUSED = auto()