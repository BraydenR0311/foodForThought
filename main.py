import pygame as pg
import time
from paths import *

pg.init()
screen = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()

# Tiles must all be the same pixel size.
TILESIZE = 75

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

    def __init__(self, *groups):
        super().__init__(*groups)
        self.index = 0
        self.screen = pg.display.get_surface()
        self.speed = 2
        self.dx = 0
        self.dy = 0
        self.image = self.up
        self.rect = self.image.get_rect(center=screen.get_rect().center)
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
        if keys[pg.K_w]:
            self.dy = -self.speed
            self._animate(self.walk_up)
            self.rect.move_ip(0, self.dy)
        if keys[pg.K_s]:
            self.dy = self.speed
            self.walking = True
            self._animate(self.walk_down)
            self.rect.move_ip(0, self.dy)
        if keys[pg.K_a]:
            self.dx = -self.speed
            self.walking = True
            self._animate(self.walk_left)
            self.rect.move_ip(self.dx, 0)
        if keys[pg.K_d]:
            self.dx = self.speed
            self.walking = True
            self._animate(self.walk_right)
            self.rect.move_ip(self.dx, 0)

    def update(self):
        self._move()

# if even gridwidth, screen center is bottomright 
#   of (gw // 2 - 1, gw // 2 - 1) grid
# if odd gridwidth screen center is center
#   of (gr // 2, gr // 2)

class Tile(pg.sprite.Sprite):
    def __init__(self, image, *groups):
        super().__init__(*groups)
        self.image = image

class Kitchen(pg.sprite.Group):

    TILE_DICT = {
        '#': pg.image.load(IMAGE_DIR / 'floor.png'),
        'x': pg.image.load(IMAGE_DIR / 'floor.png'),
        'f': pg.image.load(IMAGE_DIR / 'fryer.png'),
        'o': pg.image.load(IMAGE_DIR / 'oven.png')
    }

    def __init__(self, appliance_group, *sprites):
        super().__init__(*sprites)
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
        print(self.tilemap)

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
                self.add(new_tile)
                if tile != '#':
                    self.appliance_group.add(new_tile)


appliances = pg.sprite.Group()
players = pg.sprite.Group()
kitchen = Kitchen(appliances)
all_sprites = pg.sprite.Group(*kitchen.sprites())
player = Player(all_sprites, players)
print(appliances)
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    screen.blit(pg.image.load(IMAGE_DIR / 'background.png'))
    
    for sprite in appliances.sprites():
        if player.rect.colliderect(sprite.rect):
            if (player.rect.left < sprite.rect.right
                and player.rect.bottom > sprite.rect.top
                and player.rect.top < sprite.rect.bottom):
                player.rect.right = sprite.rect.left
            # if player.dx > 0 and player.rect.right < sprite.rect.left:
            #     player.rect.right = sprite.rect.left
            # elif player.dx < 0 and player.rect.left < sprite.rect.right:
            #     player.rect.left = sprite.rect.right
            # elif player.dy > 0 and player.rect.bottom > sprite.rect.top:
            #     player.rect.bottom = sprite.rect.top
            # elif player.dy < 0 and sprite.rect.top < sprite.rect.bottom:
            #     player.rect.top = sprite.rect.bottom
            

    print(f'dx: {player.dx}')
    print(f'dy: {player.dy}')

    all_sprites.draw(screen)
    all_sprites.update()

    pg.display.update()
    clock.tick(60)

pg.quit()