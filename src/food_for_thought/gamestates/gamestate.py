from abc import ABC, abstractmethod
from ..managers.gamestatemanager import GameStateManager
from ..managers.visualmanager import VisualManager
from ..managers.audiomanager import AudioManager


class GameState(ABC):
    def __init__(self, statekey):
        self._gsmanager: None | GameStateManager = None
        self._visualmanager: None | VisualManager = None
        self._audiomanager: None | AudioManager = None
        self.data = {}
        self._statekey = statekey
        self._issetup = False

    def set_gsmanager(self, gsmanager: GameStateManager):
        self._gsmanager = gsmanager

    def set_visualmanager(self, visualmanager: VisualManager):
        self._visualmanager = visualmanager

    def set_audiomanager(self, audiomanager: AudioManager):
        self._audiomanager = audiomanager

    def get_statekey(self):
        return self._statekey

    def update_data(self, new_data):
        self.data.update(new_data)

    def play_sound(self, sound):
        self._audiomanager.play_sound(sound)

    def issetup(self):
        return self._issetup

    def setup(self):
        self._issetup = True
        self._setup()

    def teardown(self):
        self._issetup = False
        self._teardown()

    def enter(self, *args, **kwargs):
        pass

    def exit(self, *args, **kwargs):
        pass

    @abstractmethod
    def run(self, *args, **kwargs):
        pass

    @abstractmethod
    def _setup(self, *args, **kwargs):
        pass

    @abstractmethod
    def _teardown(self, *args, **kwargs):
        pass

    @abstractmethod
    def _update(self, *args, **kwargs):
        pass

    @abstractmethod
    def _draw(self, *args, **kwargs):
        pass
