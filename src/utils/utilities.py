from constants import *
from paths import *

def read_tilemap(path, floor_cls, appliance_cls) -> pg.Rect:
    with open(path, 'r', encoding='utf-8') as infile:
            tilemap = infile.read().splitlines()

    gridwidth = len(tilemap[0])
    if gridwidth % 2 == 0:
        topleftx = (SCREEN_RECT.centerx
                    - (gridwidth // 2 * TILESIZE))
        toplefty = (SCREEN_RECT.centery
                    - (gridwidth // 2 * TILESIZE))
    else:
        topleftx = (SCREEN_RECT.centerx
                    - (gridwidth // 2 * TILESIZE)
                    - (TILESIZE // 2))
        toplefty = (SCREEN_RECT.centery
                    - (gridwidth // 2 * TILESIZE)
                    - (TILESIZE // 2))

    for i, row in enumerate(tilemap):
        for j, tile in enumerate(row):
            rect = pg.Rect(topleftx + j*TILESIZE,
                           toplefty + i*TILESIZE,
                           TILESIZE,
                           TILESIZE)
            if tile == '#':
                floor_cls(tile, rect)
            else:
                appliance_cls(tile, rect)

    kitchen_rect = pg.Rect(topleftx,
                            toplefty,
                            gridwidth * TILESIZE,
                            gridwidth * TILESIZE)

    return kitchen_rect