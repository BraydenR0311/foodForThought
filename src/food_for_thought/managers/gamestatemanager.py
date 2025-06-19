import pygame as pg

from .. import config


class MissingGamestateError(Exception):
    pass


class GameStateManager:
    def __init__(self):
        self._current_state_key = None
        self.gamestates = {}
        self.clock = pg.time.Clock()
        self._running = True

    def register_gamestate(self, gamestate, audiomanager, visualmanager):
        self.gamestates[gamestate.get_statekey()] = gamestate
        gamestate.set_gsmanager(self)
        gamestate.set_audiomanager(audiomanager)
        gamestate.set_visualmanager(visualmanager)

    def is_running(self):
        return self._running

    def quit(self):
        self._running = False

    def get_current_state(self):
        if self._current_state_key is not None:
            try:
                return self.gamestates[self._current_state_key]
            except KeyError:
                raise MissingGamestateError(
                    f"{self._current_state_key.name} statekey not registered with"
                    f" gamestatemanager."
                )

    def goto(self, statekey, data=None, teardown=False) -> None:
        if self.get_current_state() is not None:
            if teardown:
                self.get_current_state().teardown()

            self.get_current_state().exit()

        self._current_state_key = statekey

        if not self.get_current_state().issetup():
            self.get_current_state().setup()

        if data is not None:
            self.get_current_state().update_data(data)

        self.get_current_state().enter()

    def run(self):
        self.get_current_state().run()

        pg.display.flip()
        self.clock.tick(config.FPS)

    def transfer_data(self, from_statekey, to_statekey):
        try:
            from_gamestate = self.gamestates[from_statekey]
            to_gamestate = self.gamestates[to_statekey]
        except KeyError:
            print("Unable to transfer data!")
            raise

        data = from_gamestate.get_data()
        to_gamestate.update_data(data)
