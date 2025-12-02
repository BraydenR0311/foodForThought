from pathlib import Path
import pygame as pg
from typing import Iterable


class Image:
    def __init__(self, fp: Path, size: tuple[int, int] | None = None):
        self.fp = fp
        self.name = fp.stem
        self.surface = pg.image.load(self.fp)
        self.size = size or self.surface.size
        # Does nothing if size isn't supplid.
        self.surface = pg.transform.scale(self.surface, self.size)

    def get_surface(self) -> pg.Surface:
        return self.surface

    def get_rect(self, **kwargs) -> pg.Rect:
        return self.surface.get_rect(**kwargs)


class ImageCollection:
    def __init__(self, *images: Image):
        self.images = {image.name: image for image in images}

    def get_surface(self, name: str) -> pg.Surface:
        image = self.images.get(name)
        if not image:
            raise ValueError(f"Image '{name}' not found.")
        return image.get_surface()

    def get_rect(self, name: str, **kwargs) -> pg.Rect | None:
        image = self.images.get(name)
        if not image:
            return
        return image.get_rect(**kwargs)
