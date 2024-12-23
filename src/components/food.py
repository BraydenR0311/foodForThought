import pygame as pg

from paths import *
from src.components.status import Status
from src.components.generic import Generic
from src.components.tiles import Tile

class Food(pg.sprite.Sprite):

    IMAGE_DICT = {'burger': pg.image.load(IMAGE_DIR
                                          / 'burger.png').convert_alpha(),
                  'cheese': pg.image.load(IMAGE_DIR
                                          / 'cheese.png').convert_alpha(),
                  'patty': pg.image.load(IMAGE_DIR
                                          / 'patty.png').convert_alpha(),
                  'bun': pg.image.load(IMAGE_DIR
                                          / 'bun.png').convert_alpha(),
                  'patty': pg.image.load(IMAGE_DIR
                                          / 'patty.png').convert_alpha(),
                  'taco': pg.image.load(IMAGE_DIR
                                          / 'taco.png').convert_alpha(),
                'beef': pg.image.load(IMAGE_DIR
                                          / 'beef.png').convert_alpha(),
                'shell': pg.image.load(IMAGE_DIR
                                          / 'shell.png').convert_alpha(),
                'tomato': pg.image.load(IMAGE_DIR
                                          / 'tomato.png').convert_alpha()}
    
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
 
    def __init__(self, kind):
        super().__init__(self.containers)
        # ie. 'burger', 'patty'
        self.kind = kind
        self.quote = None
        
        self.status = Status(True) 

        self.appliance = self.APPLIANCE_DICT[self.kind]
        if self.appliance:
            # TODO: Access tileimages through class method
            self.appliance_hint = Generic(Tile.IMAGES[self.appliance])
            self.appliance_hint.image = pg.transform.scale_by(self.appliance_hint.image, 0.25)
            self.appliance_hint.rect = self.appliance_hint.image.get_rect()        
    
        self.image = self.IMAGE_DICT[self.kind]
        self.rect = self.image.get_rect()