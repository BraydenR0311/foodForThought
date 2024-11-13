import pygame as pg

class Text(pg.sprite.Sprite):
    def __init__(self, text, font, fontsize, color):
        super().__init__()
        self.text = text
        self.font = pg.font.Font(font, fontsize)
        self.color = color
        self.image = self.font.render(self.text, 1, self.color)
        self.rect = self.image.get_rect()