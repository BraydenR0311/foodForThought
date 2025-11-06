from . import config
from .utils.utils import get_quotes
from enum import Enum, auto

QUOTE_DATA = get_quotes(config.ASSET_DIR / "quotes.json")
