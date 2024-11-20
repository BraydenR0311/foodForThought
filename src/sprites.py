import time
from abc import ABC
import pygame as pg

from paths import *
from constants import *
from src.services import load_image

# Every sprite must have a 'containers' class variable.
# TODO: should images be stored outside of class,
#   so all in one place?

class Player(pg.sprite.Sprite):

    up_still = pg.image.load(IMAGE_DIR / 'chef' / 'chef1.png')

    down_still = pg.transform.rotate(up_still, 180)

    left_still = pg.transform.rotate(up_still, 90)

    right_still = pg.transform.rotate(up_still, 270)

    walk_up = [
        pg.image.load(IMAGE_DIR / 'chef' / 'chef2.png'),
        up_still,
        pg.image.load(IMAGE_DIR / 'chef' / 'chef3.png'),
        up_still
    ]

    walk_down = [
        pg.transform.rotate(walk_up[0], 180),
        down_still,
        pg.transform.rotate(walk_up[2], 180),
        down_still
    ]

    walk_left = [
        pg.transform.rotate(walk_up[0], 90),
        left_still,
        pg.transform.rotate(walk_up[2], 90),
        left_still
    ]

    walk_right = [
        pg.transform.rotate(walk_up[0], 270),
        right_still,
        pg.transform.rotate(walk_up[2], 270),
        right_still
    ]

    ANIM_SPEED = 0.2

    containers = None

    def __init__(self):
        super().__init__(self.containers)
        self.index = 0
        self.screen = pg.display.get_surface()
        self.speed = 2
        self.dx = 0
        self.dy = 0
        self.image = self.up_still
        self.rect = self.image.get_rect(center=self.screen.get_rect().center)
        self.time = time.time()
        self.inventory = []
        
    def animate(self, anim):
        self.elapsed = time.time() - self.time
        if self.elapsed > self.ANIM_SPEED:
            if self.index == len(anim):
                self.index = 0
            self.image = anim[self.index]
            self.time = time.time()
            self.index += 1

    def update(self):
        pass
        
# Only inherited from.
class Tile(ABC):

    TILE_IMAGES = {
        '#': load_image(IMAGE_DIR / 'floor.png'),
        'x': load_image(IMAGE_DIR / 'floor.png'),
        'f': load_image(IMAGE_DIR / 'fryer.png'),
        'p': load_image(IMAGE_DIR / 'pantry.png'),
        'o': load_image(IMAGE_DIR / 'oven.png')
    }

    containers = None

    def __init__(self, tile_type: str, rect: pg.Rect):
        super().__init__()
        self.tile_type = tile_type
        # Will overwrite this rect immediately.
        self.image, _ = self.TILE_IMAGES[self.tile_type]
        self.rect = rect
        if self.containers == None:
            raise ValueError('Must define groups for this class.')
        self.add(self.containers)

class Floor(Tile, pg.sprite.Sprite):
    def __init__(self, tile_type, rect):
        super().__init__(tile_type, rect)

class Appliance(Tile, pg.sprite.Sprite):
    def __init__(self, tile_type, rect):
        super().__init__(tile_type, rect)
        self.zone = self.rect.inflate(70, 70)
        self.popup = Foo(self.rect.center)
class Popup(pg.sprite.Sprite):

    image = load_image(IMAGE_DIR / 'e_hint.png')

    containers = None

    def __init__(self, center):
        super().__init__(self.containers)
        self.image, self.rect = self.image
        self.rect.center = center

        # self.rect.move_ip(0, -50)


# TEST
class Foo(pg.sprite.Sprite):

    image = pg.image.load(IMAGE_DIR / 'e_hint.png')

    containers = None

    def __init__(self, center):
        super().__init__()
        self.image = Foo.image
        self.rect = self.image.get_rect()

        self.rect.center = center

class Text(pg.sprite.Sprite):

    containers = None

    def __init__(self, text, font, fontsize, color, bgcolor=None):
        super().__init__(self.containers)
        self.text = text
        self.font = pg.font.Font(font, fontsize)
        self.color = color
        self.bgcolor = bgcolor
        self.image = self.font.render(self.text, 1, self.color, self.bgcolor)
        self.rect = self.image.get_rect()
        self.offset = (0, -20)

class Button(pg.sprite.Sprite):

    IMAGES = {'play': load_image(IMAGE_DIR / 'buttons' / 'play.png'),
              'play_armed': load_image(IMAGE_DIR / 'buttons' / 'play_armed.png'),
              'play_clicked': load_image(IMAGE_DIR / 'buttons' / 'play_clicked.png')}

    containers = None

    def __init__(self, button_type: str):
        super().__init__(self.containers)
        self.button_type = button_type
        self.image, self.rect = self.IMAGES[self.button_type]
        self.rect = self.align_rect()
        self.clicked = False

    def align_rect(self) -> pg.Rect:
        rect = self.image.get_rect()
        rect.center = SCREEN_RECT.center

        distance = 150
        if self.button_type == 'play':
            rect.move_ip(0, -distance)
        if self.button_type == 'quit':
            rect.move_ip(0, distance)
    
        return rect
    
    def change_image(self, image: str):
        self.image = self.images[image]

def read_tilemap(path) -> pg.Rect:
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
    # TEST
    group = pg.sprite.Group()
    for i, row in enumerate(tilemap):
        for j, tile in enumerate(row):
            rect = pg.Rect(topleftx + j*TILESIZE,
                           toplefty + i*TILESIZE,
                           TILESIZE,
                           TILESIZE)
            if tile == '#':
                Floor(tile, rect)
            else:
                Appliance(tile, rect).add(group)
                print(len(group))
                for sprite in group.sprites():
                    print(sprite.popup.rect.center)
               


            
    kitchen_rect = pg.Rect(topleftx,
                            toplefty,
                            gridwidth * TILESIZE,
                            gridwidth * TILESIZE)

    return kitchen_rect