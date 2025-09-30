import pygame as pg

from paths import *
from src.config import Config


class GameStateManager:
    def __init__(self, initial_state_id):
        self.current_state = initial_state_id
        self.gamestates = {}
        self.clock = pg.time.Clock()
        self._running = True

    def register_gamestate(self, gamestate, audiomanager, visualmanager):
        self.gamestates[gamestate.get_statekey] = gamestate
        gamestate.set_gsmanager(self)
        gamestate.set_audiomanager(audiomanager)
        gamestate.set_visualmanager(visualmanager)

    def is_running(self):
        return self._running

    def quit(self):
        self._running = False

    def get_current_state(self):
        return self.current_state

    def goto(self, statekey, data=None):
        self.current_state = statekey

        if data is not None:
            gamestate = self.gamestates[statekey]
            gamestate.update_data(data)

    def run(self):
        self.gamestates[self.current_state].run()

        pg.display.flip()
        self.clock.tick(Config.FPS)

    def transfer_data(self, from_statekey, to_statekey):
        from_gamestate = None
        to_gamestate = None
        for gamestate in self.gamestates:
            if gamestate.get_statekey() == from_statekey:
                from_gamestate = gamestate
        for gamestate in self.gamestates:
            if gamestate.get_statekey() == to_statekey:
                to_gamestate = gamestate

        if not from_gamestate or not to_gamestate:
            raise ValueError("Unable to transfer data.")
        else:
            to_gamestate.update_data(from_gamestate.get_data())
