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
