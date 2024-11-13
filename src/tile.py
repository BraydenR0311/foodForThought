import pygame as pg

class Tile(pg.sprite.Sprite):
    def __init__(self, image, *groups):
        super().__init__(*groups)
        self.image = image