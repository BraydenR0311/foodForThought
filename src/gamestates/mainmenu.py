import pygame as pg
from config import *

from src import groups
from src.components.button import Button
from src.gamestates.gamestate import GameState
from src.gamestates.statekey import StateKey


class MainMenu(GameState):
    def __init__(self, statekey):
        super().__init__(statekey)
        self.play_button = Button("play", self.visualmanager.get_screen_rect().center)
        self.quit_button = Button("quit", self.visualmanager.get_screen_rect().center)

        self.play_button.rect.move_ip(0, -100)
        self.quit_button.rect.move_ip(0, 100)

    def run(self):
        mouse_pos = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()[0]

        self.update(mouse_pos, click)
        self.draw()

        self._audiomanager.play_music()

        if self.play_button.activated:
            self.cleanup()
            self._gsmanager.goto(StateKey.PLAYING)
        elif self.quit_button.activated:
            self._gsmanager.quit()

    def update(self, mouse_pos, click):
        groups.buttons.update(mouse_pos, click)

    def draw(self):
        self.visualmanager.draw_background()
        groups.buttons.draw(self.visualmanager.get_screen())

    def cleanup(self):
        for sprite in groups.allsprites:
            sprite.kill()
