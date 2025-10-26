import json
from pathlib import Path

import pygame as pg

from .. import config


def set_sprite_images(cls):
    if not hasattr(cls, "IMAGE_PATHS"):
        raise AttributeError("Class must have IMAGE_PATHS attribute.")
    images = {
        name: pg.image.load(path).convert_alpha()
        for name, path in cls.IMAGE_PATHS.items()
    }
    cls.images = images


def get_screen_rect():
    return pg.display.get_surface().get_rect()


def read_tilemap(
    path,
    player_cls,
    floor_cls,
    appliance_cls,
    table_cls,
) -> pg.Rect:
    with open(path, "r", encoding="utf-8") as infile:
        tilemap = infile.read().splitlines()

    gridwidth = len(tilemap[0])
    if gridwidth % 2 == 0:  # Grid has even number of tiles.
        topleftx = get_screen_rect().centerx - (gridwidth // 2 * config.TILESIZE)
        toplefty = get_screen_rect().centery - (gridwidth // 2 * config.TILESIZE)
    else:  # Grid has odd number of tiles.
        topleftx = (
            get_screen_rect().centerx
            - (gridwidth // 2 * config.TILESIZE)
            - (config.TILESIZE // 2)
        )
        toplefty = (
            get_screen_rect().centery
            - (gridwidth // 2 * config.TILESIZE)
            - (config.TILESIZE // 2)
        )

    for i, row in enumerate(tilemap):
        for j, tile in enumerate(row):
            rect = pg.Rect(
                topleftx + j * config.TILESIZE,
                toplefty + i * config.TILESIZE,
                config.TILESIZE,
                config.TILESIZE,
            )
            if tile == "#":
                floor_cls(tile, rect)
            elif tile == "*":
                floor_cls("#", rect)
                player_cls(rect.center)
            elif tile == "t":
                table_cls(tile, rect)
            else:
                appliance_cls(tile, rect)

    kitchen_rect = pg.Rect(
        topleftx, toplefty, gridwidth * config.TILESIZE, gridwidth * config.TILESIZE
    )

    return kitchen_rect


def get_quotes(file: str | Path) -> list:
    """Parse json file and return dictionary in the form of
    {author: quote}
    """
    with open(file) as f:
        quotes = json.load(f)
    quotes = [
        quote
        for quote in quotes
        if config.QUOTE_MIN <= len(quote["quote"].split()) <= config.QUOTE_MAX
    ]
    return quotes
