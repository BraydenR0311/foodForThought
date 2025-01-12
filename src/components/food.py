import pygame as pg

from paths import *
from src.components.status import Status
from src.components.generic import Generic

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
    
    MENU = {
        'burger': [
            'bun',
            'patty',
            'cheese'
        ],
        'taco': [
            'shell',
            'beef',
            'tomato'
        ]
    }

    containers = None
    images = {}
 
    def __init__(self, kind, tile_images):
        super().__init__(self.containers)
        # ie. 'burger', 'patty'
        self.kind = kind
        self.tile_images = tile_images
        self.quote = None
        
        self.status = Status(True)
        self.status.kill() # It shouldn't show up at first.

        self.appliance = self.APPLIANCE_DICT[self.kind]
        if self.appliance:
            # TODO: Access tileimages through class method
            self.appliance_hint = Generic(tile_images[self.appliance])
            self.appliance_hint.image = pg.transform.scale_by(
                self.appliance_hint.image, 0.25
            )
            self.appliance_hint.rect = self.appliance_hint.image.get_rect()        
    
        self.image = self.images[self.kind]
        self.rect = self.image.get_rect()

    @classmethod
    def get_dish_names(cls):
        return list(cls.MENU.keys())
    
    @classmethod
    def get_ingredients(cls, dish_name):
        return list(cls.MENU[dish_name])
    
    @classmethod
    def get_menu(cls):
        return cls.MENU