from . import config
from .utils.utils import get_quotes

QUOTE_DATA = get_quotes(config.ASSET_DIR / "quotes.json")

TILE_IMAGE_PATHS = {
    "#": config.TILE_DIR / "floor.png",
    "x": config.TILE_DIR / "floor.png",
    "f": config.TILE_DIR / "fryer.png",
    "o": config.TILE_DIR / "oven.png",
    "c": config.TILE_DIR / "cutting.png",
    "t": config.TILE_DIR / "table.png",
}

APPLIANCE_DICT = {
    "cheese": "c",
    "patty": "o",
    "bun": "o",
    "beef": "o",
    "tomato": "c",
    "shell": "o",
}

MENU = {"burger": ["bun", "patty", "cheese"], "taco": ["shell", "beef", "tomato"]}
