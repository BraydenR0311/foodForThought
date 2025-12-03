from enum import Enum, auto


class StateKey(Enum):
    MAIN_MENU = auto()
    LEVEL = auto()
    PAUSED = auto()
    COOK = auto()
    INITIALIZING_ROUND = auto()
    GAME_OVER = auto()
