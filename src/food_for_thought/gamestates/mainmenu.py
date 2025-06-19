import pygame as pg


from .. import groups
from ..components.button import Button
from .gamestate import GameState
from .statekey import StateKey


class MainMenu(GameState):
    def __init__(self, statekey):
        super().__init__(statekey)

    def _setup(self):
        self.play_button = Button("play", self._visualmanager.get_screen_rect().center)
        self.quit_button = Button("quit", self._visualmanager.get_screen_rect().center)

        self.play_button.rect.move_ip(0, -100)
        self.quit_button.rect.move_ip(0, 100)

    def run(self):
        self._update()
        self._draw()

        self._audiomanager.play_music()

        if self.play_button.activated:
            self._gsmanager.goto(StateKey.LEVEL, teardown=True)
        elif self.quit_button.activated:
            self._gsmanager.quit()

    def _update(self):
        mouse_pos = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()[0]
        groups.buttons.update(mouse_pos, click)

    def _draw(self):
        self._visualmanager.draw_background()
        groups.buttons.draw(self._visualmanager.get_screen())

    def _teardown(self):
        for sprite in groups.all_sprites:
            sprite.kill()
