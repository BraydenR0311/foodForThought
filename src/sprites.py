import time
import pygame as pg
from paths import *
from constants import *

class Kitchen(pg.sprite.Group):

    TILE_DICT = {
        '#': pg.image.load(IMAGE_DIR / 'floor.png'),
        'x': pg.image.load(IMAGE_DIR / 'floor.png'),
        'f': pg.image.load(IMAGE_DIR / 'fryer.png'),
        'p': pg.image.load(IMAGE_DIR / 'pantry.png'),
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
                new_tile.player_group = self.player_group
                new_tile.tile = tile
                new_tile.rect = pg.Rect(
                    self.topleftx + (j * TILESIZE),
                    self.toplefty + (i * TILESIZE),
                    TILESIZE,
                    TILESIZE
                )
                self.add(new_tile)
                if tile != '#':
                    self.appliance_group.add(new_tile)

class Player(pg.sprite.Sprite):

    up = pg.image.load(IMAGE_DIR / 'chef' / 'chef1.png')

    down = pg.transform.rotate(up, 180)

    left = pg.transform.rotate(up, 90)

    right = pg.transform.rotate(up, 270)

    walk_up = [
        pg.image.load(IMAGE_DIR / 'chef' / 'chef2.png'),
        up,
        pg.image.load(IMAGE_DIR / 'chef' / 'chef3.png'),
        up
    ]

    walk_down = [
        pg.transform.rotate(walk_up[0], 180),
        down,
        pg.transform.rotate(walk_up[2], 180),
        down
    ]

    walk_left = [
        pg.transform.rotate(walk_up[0], 90),
        left,
        pg.transform.rotate(walk_up[2], 90),
        left
    ]

    walk_right = [
        pg.transform.rotate(walk_up[0], 270),
        right,
        pg.transform.rotate(walk_up[2], 270),
        right
    ]

    ANIM_SPEED = 0.2

    def __init__(self, collide_group, kitchen):
        super().__init__()
        self.collide_group = collide_group
        self.kitchen = kitchen
        self.index = 0
        self.screen = pg.display.get_surface()
        self.speed = 2
        self.dx = 0
        self.dy = 0
        self.image = self.up
        self.rect = self.image.get_rect(center=self.screen.get_rect().center)
        self.time = time.time()
        
    def _animate(self, anim):
        self.elapsed = time.time() - self.time
        if self.elapsed > self.ANIM_SPEED:
            if self.index == len(anim):
                self.index = 0
            self.image = anim[self.index]
            self.time = time.time()
            self.index += 1

    def _move(self):
        keys = pg.key.get_pressed()
        self.dx = 0
        self.dy = 0
        if keys[pg.K_LSHIFT]:
            self.speed = 4
        else:
            self.speed = 2
        
        
        if keys[pg.K_w]:
            self.dy = -self.speed
            self._animate(self.walk_up)
            self.rect.move_ip(0, self.dy)
        if keys[pg.K_s]:
            self.dy = self.speed
            self._animate(self.walk_down)
            self.rect.move_ip(0, self.dy)
        
        hitlist = pg.sprite.spritecollide(self, self.collide_group, False)
        for sprite in hitlist:
            if self.dy > 0:
                self.rect.bottom = sprite.rect.top
            elif self.dy < 0:
                self.rect.top = sprite.rect.bottom

        if keys[pg.K_a]:
            self.dx = -self.speed
            self._animate(self.walk_left)
            self.rect.move_ip(self.dx, 0)
        if keys[pg.K_d]:
            self.dx = self.speed
            self._animate(self.walk_right)
            self.rect.move_ip(self.dx, 0)

        hitlist = pg.sprite.spritecollide(self, self.collide_group, False)
        for sprite in hitlist:
            if self.dx > 0:
                self.rect.right = sprite.rect.left 
            elif self.dx < 0:
                self.rect.left = sprite.rect.right

    def update(self):
        self._move()
        self.rect = self.rect.clamp(self.kitchen.rect)

class Tile(pg.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.tile = None
        self.player_group = None
        self.image = image
        self.rect = self.image.get_rect()
        self.hitbox = self.rect.inflate(20, 20)
        self.text = Text('foo',
                         ASSET_DIR / 'fonts' / 'pixel.ttf',
                         10,
                         'black')
    
    def update(self):
        if self.tile == 'p':
            if self.hitbox.colliderect(self.player_group):
                print('foo')
class Text(pg.sprite.Sprite):
    def __init__(self, text, font, fontsize, color):
        super().__init__()
        self.text = text
        self.font = pg.font.Font(font, fontsize)
        self.color = color
        self.image = self.font.render(self.text, 1, self.color)
        self.rect = self.image.get_rect()
        self.offset = (0, -20)