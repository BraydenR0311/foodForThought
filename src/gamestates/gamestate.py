from abc import ABC, abstractmethod

from paths import *


class GameState(ABC):
    def __init__(self, statekey, gsmanager):
        self.statekey = statekey
        self.gsmanager = gsmanager
        self.data = {}

    def get_statekey(self):
        return self.statekey

    def update_data(self, new_data):
        self.data.update(new_data)

    def get_data(self):
        return self.data

    def request(self, from_statekey, to_statekey):
        self.gsmanager.transfer_data(from_statekey, to_statekey)

    @abstractmethod
    def run(self, data):
        pass

    @abstractmethod
    def cleanup(self):
        pass

    @abstractmethod
    def respond(self):
        pass
