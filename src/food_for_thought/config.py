from pathlib import Path

# Paths.
PROJ_ROOT = Path(__file__).parents[2]
ASSET_DIR = PROJ_ROOT / "assets"
IMAGE_DIR = ASSET_DIR / "images"

FOOD_DIR = IMAGE_DIR / "food"
TILE_DIR = IMAGE_DIR / "tiles"
POPUP_DIR = IMAGE_DIR / "popups"
TICKET_DIR = IMAGE_DIR / "ticket"
FACES_DIR = IMAGE_DIR / "faces"

AUDIO_DIR = ASSET_DIR / "audio"
MUSIC_DIR = AUDIO_DIR / "music"
SOUND_DIR = AUDIO_DIR / "sounds"
FONT_DIR = ASSET_DIR / "fonts"

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
