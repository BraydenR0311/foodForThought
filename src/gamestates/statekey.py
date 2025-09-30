from enum import Enum, auto


class StateKey(Enum):
    MAIN_MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    TYPING = auto()
    INITIALIZING_ROUND = auto()
