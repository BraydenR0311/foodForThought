from enum import Enum, auto

class Gamestate(Enum):
    MAIN_MENU = auto()
    PLAYING = auto()
    PAUSED = auto()