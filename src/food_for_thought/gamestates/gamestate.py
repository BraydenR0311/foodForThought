from abc import ABC, abstractmethod


class GameState(ABC):
    def __init__(self, statekey):
        self.data = {}
        self._statekey = statekey
        self._is_setup = False

    def get_statekey(self):
        return self._statekey

    def update_data(self, new_data):
        self.data.update(new_data)

    def enter(self, *args, **kwargs):
        if not self._is_setup:
            self._is_setup = True
            self._setup()
        self._enter()

    def exit(self, teardown=False, *args, **kwargs):
        self._exit()
        if teardown:
            self._is_setup = False

            self._teardown()

    @abstractmethod
    def run(self, *args, **kwargs):
        pass

    @abstractmethod
    def _setup(self, *args, **kwargs):
        pass

    def _enter(self, *args, **kwargs):
        pass

    @abstractmethod
    def _teardown(self, *args, **kwargs):
        pass

    def _exit(self, *args, **kwargs):
        pass

    @abstractmethod
    def _update(self, *args, **kwargs):
        pass

    @abstractmethod
    def _draw(self, *args, **kwargs):
        pass
