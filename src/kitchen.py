import pygame as pg
from paths import *
from constants import *
from src.tile import Tile

class Kitchen(pg.sprite.Group):

    TILE_DICT = {
        '#': pg.image.load(IMAGE_DIR / 'floor.png'),
        'x': pg.image.load(IMAGE_DIR / 'floor.png'),
        'f': pg.image.load(IMAGE_DIR / 'fryer.png'),
        'o': pg.image.load(IMAGE_DIR / 'oven.png')
    }

    def __init__(self, appliance_group):
        super().__init__()
        self.screen = pg.display.get_surface()

        with open(ROOT_DIR / 'map1', 'r', encoding='utf-8') as infile:
            self.tilemap = infile.read().splitlines()

        self.gridwidth = len(self.tilemap[0])
        if self.gridwidth % 2 == 0:
            self.topleftx = self.screen.get_rect().centerx - (self.gridwidth // 2 * TILESIZE)
            self.toplefty = self.screen.get_rect().centery - (self.gridwidth // 2 * TILESIZE)
        else:
            self.topleftx = (self.screen.get_rect().centerx
                             - (self.gridwidth // 2 * TILESIZE)
                             - (TILESIZE // 2))
            self.toplefty = (self.screen.get_rect().centery
                             - (self.gridwidth // 2 * TILESIZE)
                             - (TILESIZE // 2))

        self.appliance_group = appliance_group
        self.read_tilemap(self.tilemap)
        self.rect = pg.Rect(*self.sprites()[0].rect.topleft, self.gridwidth * TILESIZE, self.gridwidth * TILESIZE)

    def read_tilemap(self, tilemap):
        for i, row in enumerate(tilemap):
            for j, tile in enumerate(row):
                new_tile = Tile(self.TILE_DICT[tile])
                new_tile.rect = pg.Rect(
                    self.topleftx + (j * TILESIZE),
                    self.toplefty + (i * TILESIZE),
                    TILESIZE,
                    TILESIZE
                )
                new_tile.hitbox = new_tile.rect.inflate(20, 20)
                self.add(new_tile)
                if tile != '#':
                    self.appliance_group.add(new_tile)