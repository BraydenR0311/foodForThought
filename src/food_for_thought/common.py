from . import config
from .utils.utils import get_quotes

QUOTE_DATA = get_quotes(config.ASSET_DIR / "quotes.json")
