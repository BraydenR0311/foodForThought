from enum import Enum, auto

class Gamestate(Enum):
    MAIN_MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    TYPING = auto()

# TODO: Change to MAIN_MENU
global_state = Gamestate.MAIN_MENU