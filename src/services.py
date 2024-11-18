from typing import Tuple
import pygame as pg

from paths import *
from constants import *

def load_image(path: str) -> Tuple[pg.Surface, pg.Rect]:
    """Load image and return image object"""
    imagefile = path
    try:
        image = pg.image.load(imagefile)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except FileNotFoundError:
        print(f"Cannot load image: {imagefile}")
        raise SystemExit
    return image, image.get_rect()
