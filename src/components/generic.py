import pygame as pg

class Generic(pg.sprite.Sprite):
    """
    For any type of image that needs to be blitted onto the screen, but with
    wrapped in a class for sprite-like control.
    """

    containers = None

    def __init__(self, image):
        super().__init__(self.containers)
        self.image = image
        self.rect = self.image.get_rect()