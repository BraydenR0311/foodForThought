import random
from pathlib import Path

import pygame as pg

from paths import *
from src.config import Config

def set_sprite_images(cls):
    if not hasattr(cls, 'IMAGE_PATHS'):
        raise AttributeError('Class must have IMAGE_PATHS attribute.')
    images = {name: pg.image.load(path).convert_alpha()
              for name, path in cls.IMAGE_PATHS.items()}
    cls.images = images

def get_screen_rect():
    return pg.display.get_surface().get_rect()

def read_tilemap(path, floor_cls, appliance_cls) -> pg.Rect:
    with open(path, 'r', encoding='utf-8') as infile:
            tilemap = infile.read().splitlines()

    gridwidth = len(tilemap[0])
    if gridwidth % 2 == 0:
        topleftx = (get_screen_rect().centerx
                    - (gridwidth // 2 * Config.TILESIZE))
        toplefty = (get_screen_rect().centery
                    - (gridwidth // 2 * Config.TILESIZE))
    else:
        topleftx = (get_screen_rect().centerx
                    - (gridwidth // 2 * Config.TILESIZE)
                    - (Config.TILESIZE // 2))
        toplefty = (get_screen_rect().centery
                    - (gridwidth // 2 * Config.TILESIZE)
                    - (Config.TILESIZE // 2))

    for i, row in enumerate(tilemap):
        for j, tile in enumerate(row):
            rect = pg.Rect(topleftx + j*Config.TILESIZE,
                           toplefty + i*Config.TILESIZE,
                           Config.TILESIZE,
                           Config.TILESIZE)
            if tile == '#':
                floor_cls(tile, rect)
            else:
                appliance_cls(tile, rect)

    kitchen_rect = pg.Rect(topleftx,
                            toplefty,
                            gridwidth * Config.TILESIZE,
                            gridwidth * Config.TILESIZE)

    return kitchen_rect



def quotegen(quotes: dict) -> tuple[str, str]:
    """
    Returns a tuple of an author and one of their quotes.
    """
    
    author = random.choice(list(quotes.keys()))
    quote = random.choice(quotes[author])

    return author, quote

def quoteread(file: str | Path) -> dict[str, list]:
    """
    Read quotes.txt and return dictionary in the form of {author: quote}
    """

    quotes = {}
    author = None

    with open(file, 'r', encoding='utf-8') as infile:
        for line in infile:
            line = line.strip()
            # Empty lines separate author/quote blocks
            if not line:
                author = None
            # Found an author
            elif not author:
                author = line
                quotes[author] = []
            else:
                quotes[author].append(line)

    return quotes
