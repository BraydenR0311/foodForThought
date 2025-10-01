from abc import ABC, abstractmethod

from config import *


class GameState(ABC):
    def __init__(self, statekey):
        self._statekey = statekey
        self.gsmanager = None
        self.visualmanager = None
        self.audiomanager = None
        self.data = {}

    def set_gsmanager(self, gsmanager):
        self.gsmanager = gsmanager

    def set_audiomanager(self, audiomanager):
        self.audiomanager = audiomanager

    def set_visualmanager(self, visualmanager):
        self.visualmanager = visualmanager

    def get_statekey(self):
        return self._statekey

    def update_data(self, new_data):
        self.data.update(new_data)

    def goto(self, statekey, data=None):
        self.gsmanager.goto(statekey, data)

    def play_sound(self, sound):
        self.audiomanager.play_sound(sound)

    def setup(self):
        pass

    def cleanup(self):
        pass

    def run(self):
        pass

    def update(self):
        pass
