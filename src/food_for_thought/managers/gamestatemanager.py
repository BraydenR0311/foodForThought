from typing import TYPE_CHECKING, Any

import pygame as pg

from .. import config
import logging
import sys

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from ..gamestates.gamestate import GameState

from ..gamestates.statekey import StateKey


class MissingGamestateError(Exception):
    pass


class GameStateManager:
    _instance = None
    _initialized = False

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if GameStateManager._initialized:
            return
        GameStateManager._initialized = True
        self._current_statekey = StateKey.MAIN_MENU
        self._gamestates = {}
        self.clock = pg.time.Clock()
        self._running = True

    def register_gamestate(self, *gamestates: "GameState"):
        for gs in gamestates:
            self._gamestates[gs.get_statekey()] = gs

    def is_running(self):
        return self._running

    def quit(self):
        self._running = False

    def goto(self, statekey, data: dict[str, Any] | None = None, teardown=False) -> None:
        current_state = self.get_current_state()
        current_state.exit(teardown)

        self._current_statekey = statekey
        new_state = self.get_current_state()

        if data is not None:
            self.send_data(data)

        new_state.enter()

    def get_current_state(self) -> "GameState":
        try:
            gs = self._gamestates[self._current_statekey]
        except KeyError:
            logger.error("Cannot find gamestate. Maybe it isn't registered yet.")
            sys.exit(1)
        return gs

    def run(self):
        dt = self.clock.tick(config.FPS) / 1000
        events = pg.event.get()

        for event in events:
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.quit()

        # Make sure current state has a copy of the current events.
        self.send_data({"events": events, "dt": dt})
        self.get_current_state().run()

        pg.display.flip()

    def send_data(self, data: dict[str, Any]) -> None:
        self.get_current_state().update_data(data)
