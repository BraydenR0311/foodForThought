import pygame as pg

from paths import *
from src.config import Config


class GameStateManager:
    def __init__(self, initial_state_id, gamestates):
        self.current_state = initial_state_id
        self.gamestates = gamestates
        self._running = True

    def is_running(self):
        return self._running

    def exit(self):
        self._running = False

    def get_current_state(self):
        return self.current_state

    def goto(self, state_id):
        self.current_state = state_id

    def run(self):
        for gamestate in self.gamestates:
            if gamestate.state_id == self.current_state:
                gamestate.run()

    def transfer_data(self, from_statekey, to_statekey):
        from_gamestate = None
        to_gamestate = None
        for gamestate in gamestate:
            if gamestate.get_statekey() == from_statekey:
                from_gamestate = gamestate
            elif gamestate.get_statekey() == to_statekey:
                to_gamestate = gamestate

        if not from_gamestate and not to_gamestate:
            print("No data found.")
        else:
            to_gamestate.update_data(from_gamestate.get_data())
