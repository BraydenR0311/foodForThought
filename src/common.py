from config import *
from src.utils.utils import get_quotes

QUOTE_DATA = get_quotes(ASSET_DIR / "quotes.json")

TILE_IMAGE_PATHS = {
    "#": TILE_DIR / "floor.png",
    "x": TILE_DIR / "floor.png",
    "f": TILE_DIR / "fryer.png",
    "o": TILE_DIR / "oven.png",
    "c": TILE_DIR / "cutting.png",
    "t": TILE_DIR / "table.png",
}

MENU = {"burger": ["bun", "patty", "cheese"], "taco": ["shell", "beef", "tomato"]}
