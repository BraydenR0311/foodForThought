import pygame as pg

from paths import *
from src.components.status import Status
from src.components.generic import Generic
from src.components.tiles import Tile

class Food(pg.sprite.Sprite):

    IMAGE_PATHS = {'burger': IMAGE_DIR / 'burger.png',
                  'cheese': IMAGE_DIR / 'cheese.png',
                  'patty': IMAGE_DIR / 'patty.png',
                  'bun': IMAGE_DIR / 'bun.png',
                  'patty': IMAGE_DIR / 'patty.png',
                  'taco': IMAGE_DIR / 'taco.png',
                  'beef': IMAGE_DIR / 'beef.png',
                  'shell': IMAGE_DIR / 'shell.png',
                  'tomato': IMAGE_DIR / 'tomato.png'}
    
    APPLIANCE_DICT = {'burger': None,
                    'cheese': 'c',
                  'patty': 'o',
                  'bun': 'o',
                  'taco': None,
                  'beef': 'o',
                  'tomato': 'c',
                  'shell': 'o'}
    
    DISH_DICT = {'burger': ['bun',
                            'patty',
                            'cheese'],
                 'taco': ['shell',
                          'beef',
                          'tomato']}

    containers = None
    images = {}
 
    def __init__(self, kind):
        super().__init__(self.containers)
        # ie. 'burger', 'patty'
        self.kind = kind
        self.quote = None
        
        self.status = Status(True)
        # It shouldn't show up at first.
        self.status.kill()

        self.appliance = self.APPLIANCE_DICT[self.kind]
        if self.appliance:
            # TODO: Access tileimages through class method
            self.appliance_hint = Generic(Tile.images[self.appliance])
            self.appliance_hint.image = pg.transform.scale_by(self.appliance_hint.image, 0.25)
            self.appliance_hint.rect = self.appliance_hint.image.get_rect()        
    
        self.image = self.images[self.kind]
        self.rect = self.image.get_rect()