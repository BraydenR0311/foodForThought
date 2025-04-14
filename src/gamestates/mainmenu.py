import pygame as pg

from src import groups
from src.components.button import Button
from src.gamestates.gamestate import GameState
from src.gamestates.statekey import StateKey


class MainMenu(GameState):
    def __init__(
        self, statekey, gsmanager, audiomanager, visualmanager, allsprites
    ):
        super().__init__(statekey, gsmanager)
        self.audiomanager = audiomanager
        self.visualmanager = visualmanager
        self.allsprites = allsprites
        self.buttons = groups.buttons
        self.play_button = Button("play")
        self.quit_button = Button("quit")

    def run(self):
        mouse_pos = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()[0]

        self.update(mouse_pos, click)
        self.draw()

        self.audiomanager.play_music()

        if self.play_button.is_activated():
            self.cleanup()
            self.gsmanager.goto(StateKey.PLAYING)
        elif self.quit_button.is_activated():
            self.gsmanager.exit()

    def update(self, mouse_pos, click):
        self.buttons.update(mouse_pos, click)

    def draw(self):
        self.visualmanager.draw_background()
        self.buttons.draw()

    def cleanup(self):
        for sprite in allsprites:
            sprite.kill()
