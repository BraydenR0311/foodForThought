import pygame as pg
from paths import *

class Config:
    # Screen dimensions.
    WIDTH = 1280
    HEIGHT = 720
    FPS = 60

    # Kitchen tiles should be same pixel size.
    TILESIZE = 75

    # Quote constants.
    QUOTE_MIN = 12
    QUOTE_MAX = 40

    # Fonts.
    DEFAULT_FONT = FONT_DIR / 'pixel.ttf'
