from pathlib import Path


class Config:
    # Screen dimensions.
    WIDTH = 1280
    HEIGHT = 720
    FPS = 60

    # Kitchen tiles should be same pixel size.
    TILESIZE = 75

    # Quote constants.
    QUOTE_MIN = 12
    QUOTE_MAX = 40

    # Fonts.
    DEFAULT_FONT = FONT_DIR / "pixel.ttf"


ASSET_DIR = Path("assets")
IMAGE_DIR = ASSET_DIR / "images"

FOOD_DIR = IMAGE_DIR / "food"
TILE_DIR = IMAGE_DIR / "tiles"
POPUP_DIR = IMAGE_DIR / "popups"

AUDIO_DIR = ASSET_DIR / "audio"
FONT_DIR = ASSET_DIR / "fonts"
