from abc import ABC, abstractmethod


class GameState(ABC):
    def __init__(self, statekey):
        self._gsmanager = None
        self._visualmanager = None
        self._audiomanager = None
        self.data = {}
        self._statekey = statekey
        self._issetup = False

    def set_gsmanager(self, gsmanager):
        self._gsmanager = gsmanager

    def set_audiomanager(self, audiomanager):
        self._audiomanager = audiomanager

    def set_visualmanager(self, visualmanager):
        self._visualmanager = visualmanager

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
