from typing import Any

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

    def goto(
        self, statekey, data: dict[str, Any] | None = None, teardown=False
    ) -> None:
        current_state = self.get_current_state()
        if current_state is not None:
            current_state.exit()
            if teardown:
                current_state.teardown()

        self._current_state_key = statekey
        current_state = self.get_current_state()

        if data is not None:
            self.send_data(data)

        if not current_state.issetup():
            current_state.setup()

        current_state.enter()

    def get_current_state(self):
        if self._current_state_key is not None:
            try:
                return self.gamestates[self._current_state_key]
            except KeyError:
                raise MissingGamestateError(
                    f"{self._current_state_key.name} statekey not registered with"
                    f" gamestatemanager."
                )

    def run(self):
        self.get_current_state().run()

        pg.display.flip()
        self.clock.tick(config.FPS)

    def send_data(self, data: dict[str, Any]) -> None:
        self.get_current_state().update_data(data)
