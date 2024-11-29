import time
import string
from abc import ABC
import pygame as pg

from paths import *
from constants import *
from src.gamestate import Gamestate
from src.services import quotegen

# Every sprite must have a 'containers' class variable.
# TODO: should images be stored outside of class,
#   so all in one place?
# TODO: change 'food' to dish, removing ambiguity of food vs. ingredient
# TODO: one button class

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

    def update(self):
        self.center_vec = pg.math.Vector2(*self.rect.center)

    def animate(self, anim):
        self.elapsed = time.time() - self.time
        if self.elapsed > self.ANIM_SPEED:
            if self.index == len(anim):
                self.index = 0
            self.image = anim[self.index]
            self.time = time.time()
            self.index += 1
        
# Only inherited from.
class Tile(ABC):

    TILE_IMAGES = {
        '#': pg.image.load(IMAGE_DIR / 'floor.png'),
        'x': pg.image.load(IMAGE_DIR / 'floor.png'),
        'f': pg.image.load(IMAGE_DIR / 'fryer.png'),
        'p': pg.image.load(IMAGE_DIR / 'pantry.png'),
        'o': pg.image.load(IMAGE_DIR / 'oven.png'),
        'c': pg.image.load(IMAGE_DIR / 'cutting.png')
    }

    containers = None

    def __init__(self, kind: str, rect: pg.Rect):
        super().__init__()
        self.kind = kind
        # Will overwrite this rect immediately.
        self.image = self.TILE_IMAGES[self.kind]
        self.rect = rect
        if self.containers == None:
            raise ValueError('Must define groups for this class.')
        self.add(self.containers)

class Floor(Tile, pg.sprite.Sprite):
    def __init__(self, kind, rect):
        super().__init__(kind, rect)

class Appliance(Tile, pg.sprite.Sprite):

    def __init__(self, kind, rect):
        super().__init__(kind, rect)
        self.zone = self.rect.inflate(70, 70)
        self.popup = Popup(self.rect.center)
        self.center_vec = pg.math.Vector2(*self.rect.center)
        
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

class Quote(Text):

    containers = None

    def __init__(self, text, font, fontsize, color, bgcolor=None):
        super().__init__(text, font, fontsize, color, bgcolor)
        # User input used to color text.
        self.user = Text('', ASSET_DIR / 'fonts' /'pixel.ttf', 20, 'green')
        self.rect.center = SCREEN_RECT.center
        self.rect = self.rect.move(0, -SCREEN_RECT.height // 3)
        self.user.rect = self.rect
        self.wrongs = 0
        self.wronged = False

    def update(self):
        self.image = self.font.render(self.text, 1, self.color, self.bgcolor)
        if (not self.text.startswith(self.user.text) and
            not self.wronged):
            self.wronged = not self.wronged
            self.color = 'red'
            self.wrongs += 1
            
        elif self.text.startswith(self.user.text):
            if self.wronged:
                self.wronged = not self.wronged
            self.color = 'black'
            self.user.image = self.font.render(self.user.text, 1, self.user.color)

    # Needs pg.event.get() as events
    def type_out(self, events):
        for event in events:
            if event.type == pg.TEXTINPUT:
                if (event.text in string.ascii_letters
                    + string.digits
                    + string.punctuation
                    +  ' ' and
                    not self.wronged):
                    self.user.text = self.user.text + event.text
            elif (event.type == pg.KEYDOWN and
                  event.key == pg.K_BACKSPACE):
                    self.user.text = self.user.text[:-1]
        
        if self.user.text == self.text:
            self.user.kill()
            self.kill()
            
class Food(pg.sprite.Sprite):

    IMAGE_DICT = {'burger': pg.image.load(IMAGE_DIR
                                          / 'burger'
                                          / 'burger.png'),
                  'cheese': pg.image.load(IMAGE_DIR
                                          / 'burger'
                                          / 'cheese.png'),
                  'patty': pg.image.load(IMAGE_DIR
                                          / 'burger'
                                          / 'patty.png'),
                  'bun': pg.image.load(IMAGE_DIR
                                          / 'burger'
                                          / 'bun.png'),
                  'patty': pg.image.load(IMAGE_DIR
                                          / 'burger'
                                          / 'patty.png')}
    
    APPLIANCE_DICT = {'burger': None,
                  'cheese': 'c',
                  'patty': 'g',
                  'bun': 'g',}
    
    FOOD_DICT = {'burger': ['bun',
                            'patty',
                            'cheese']}

    containers = None
 
    def __init__(self, kind):
        super().__init__(self.containers)
        # ie. 'burger', 'patty'
        self.kind = kind
        self.quote = None

        self.image = self.IMAGE_DICT[self.kind]
        self.rect = self.image.get_rect()

    @staticmethod
    def split_quote(quote, index):
        quote = quote.split()
        chunk_len = len(quote) // 3

        first = ' '.join(quote[:chunk_len])
        second = ' '.join(quote[chunk_len:2 * chunk_len])
        third = ' '.join(quote[2 * chunk_len:])

        quotes = first, second, third

        return quotes[index]


class Ticket(pg.sprite.Sprite):

    containers = None

    def __init__(self, dish):
        super().__init__(self.containers)
        self.size = (100, 150)
        self.offset = 10
        
        self.image = pg.Surface(self.size)
        self.image.fill('white')
        self.rect = self.image.get_rect()
        self.rect.move_ip(self.offset, self.offset)
        
        self.author, self.quote = quotegen(QUOTES)

        self.dish = Food(dish)
        self.dish.rect.bottomleft = self.rect.bottomleft

        self.ingredients = [Food(ingredient)
                            for ingredient in Food.FOOD_DICT[dish]]
        self.ingredient_offset = 30
        for i, ingredient in enumerate(self.ingredients):
            ingredient.rect.topleft = self.rect.topleft
            ingredient.rect.move_ip(0, i*self.ingredient_offset)
            ingredient.quote = Quote(ingredient.split_quote(self.quote, i),
                                     ASSET_DIR / 'fonts' / 'pixel.ttf',
                                     20,
                                     'black')
        
    def update(self):
        pass

class Popup(pg.sprite.Sprite):

    IMAGE = pg.image.load(IMAGE_DIR / 'e_hint.png')

    containers = None

    def __init__(self, center):
        super().__init__(self.containers)
        self.image = self.IMAGE
        self.rect = self.image.get_rect(midbottom=center)
        self.rect.move_ip(0, -25)
        self.kill()

    def update(self):
        pass

class Button(pg.sprite.Sprite):

    IMAGES = {'play': pg.image.load(IMAGE_DIR
                                    / 'buttons'
                                    / 'play.png'),
              'play_armed': pg.image.load(IMAGE_DIR
                                          / 'buttons'
                                          / 'play_armed.png'),
              'play_clicked': pg.image.load(IMAGE_DIR                                         
                                            / 'buttons'
                                            / 'play_clicked.png')}

    containers = None

    def __init__(self, button_type: str):
        super().__init__(self.containers)
        self.button_type = button_type
        self.image = self.IMAGES[self.button_type]
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

    for i, row in enumerate(tilemap):
        for j, tile in enumerate(row):
            rect = pg.Rect(topleftx + j*TILESIZE,
                           toplefty + i*TILESIZE,
                           TILESIZE,
                           TILESIZE)
            if tile == '#':
                Floor(tile, rect)
            else:
                Appliance(tile, rect)

    kitchen_rect = pg.Rect(topleftx,
                            toplefty,
                            gridwidth * TILESIZE,
                            gridwidth * TILESIZE)

    return kitchen_rect