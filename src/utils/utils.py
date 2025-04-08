import random
import json
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

def read_tilemap(path,
    floor_cls,
    appliance_cls,
    table_cls,
    dish_names
) -> pg.Rect:
    with open(path, 'r', encoding='utf-8') as infile:
            tilemap = infile.read().splitlines()

    gridwidth = len(tilemap[0])
    if gridwidth % 2 == 0: # Grid has even number of tiles.
        topleftx = (get_screen_rect().centerx
                    - (gridwidth // 2 * Config.TILESIZE))
        toplefty = (get_screen_rect().centery
                    - (gridwidth // 2 * Config.TILESIZE))
    else: # Grid has odd number of tiles.
        topleftx = (get_screen_rect().centerx
                    - (gridwidth // 2 * Config.TILESIZE)
                    - (Config.TILESIZE // 2))
        toplefty = (get_screen_rect().centery
                    - (gridwidth // 2 * Config.TILESIZE)
                    - (Config.TILESIZE // 2))

    for i, row in enumerate(tilemap):
        for j, tile in enumerate(row):
            rect = pg.Rect(
                topleftx + j*Config.TILESIZE,
                toplefty + i*Config.TILESIZE,
                Config.TILESIZE,
                Config.TILESIZE
            )
            if tile == '#':
                floor_cls(tile, rect)
            elif tile == 't':
                table_cls(tile, rect, dish_names)
            else:
                appliance_cls(tile, rect)

    kitchen_rect = pg.Rect(
        topleftx,
        toplefty,
        gridwidth * Config.TILESIZE,
        gridwidth * Config.TILESIZE
    )

    return kitchen_rect


def get_quotes(file: str | Path) -> dict[str, list]:
    """Parse json file and return dictionary in the form of
    {author: quote}
    """
    with open(file) as infile:
        quotes = json.load(infile)
    quotes = [
        quote for quote in quotes
        if Config.QUOTE_MIN<= len(quote['quote'].split()) <= Config.QUOTE_MAX
    ]
    return quotes
