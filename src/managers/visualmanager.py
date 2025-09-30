import pygame as pg

from paths import *
from src.config import Config


class VisualManager:
    def __init__(self):
        self._screen = self.load_screen()
        self.background_img = pg.image.load(
            IMAGE_DIR / "background.png"
        ).convert_alpha()

    def load_screen(self):
        return pg.display.set_mode((Config.WIDTH, Config.HEIGHT))

    def get_screen(self):
        return self._screen

    def get_screen_rect(self):
        return self.get_screen().get_rect()

    def draw_background(self):
        self.get_screen().blit(self.background_img, (0, 0))

    def draw(self, *groups):
        """Draws groups to the screen in order listed."""
        for group in groups:
            group.draw(self.get_screen())

    @staticmethod
    def set_sprite_images(sprite_class):
        """Convert all images that belong to a sprite.

        This is necessary you can't convert images before pg.init()
        which happens in main() after all module are imported.
        """
        if not hasattr(sprite_class, "IMAGE_PATHS"):
            raise AttributeError("Class must have IMAGE_PATHS attribute.")
        images = {
            name: pg.image.load(path).convert_alpha()
            for name, path in sprite_class.IMAGE_PATHS.items()
        }
        sprite_class.images = images
