from paths import *
from src.utils.utils import get_quotes

QUOTE_DATA = get_quotes(ASSET_DIR / 'quotes.json')

TILE_IMAGE_PATHS = {
        '#': IMAGE_DIR / 'floor.png',
        'x': IMAGE_DIR / 'floor.png',
        'f': IMAGE_DIR / 'fryer.png',
        'p': IMAGE_DIR / 'pantry.png',
        'o': IMAGE_DIR / 'oven.png',
        'c': IMAGE_DIR / 'cutting.png',
        't': IMAGE_DIR / 'table.png'
    }

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
