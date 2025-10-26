import pygame as pg


from .. import groups
from ..components.button import Button
from .gamestate import GameState
from .statekey import StateKey
from ..managers.visualmanager import VisualManager
from ..managers.audiomanager import AudioManager
from ..managers.gamestatemanager import GameStateManager

gamestate_manager = GameStateManager()
audio_manager = AudioManager()
visual_manager = VisualManager()


class MainMenu(GameState):
    def __init__(self):
        super().__init__(StateKey.MAIN_MENU)

    def _setup(self):
        self.play_button = Button("play", visual_manager.get_screen_rect().center)
        self.quit_button = Button("quit", visual_manager.get_screen_rect().center)

        self.play_button.rect.move_ip(0, -100)
        self.quit_button.rect.move_ip(0, 100)

    def run(self):
        self._update()
        self._draw()

        audio_manager.play_music()

        if self.play_button.activated:
            gamestate_manager.goto(StateKey.LEVEL, teardown=True)
        elif self.quit_button.activated:
            gamestate_manager.quit()

    def _update(self):
        mouse_pos = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()[0]
        groups.buttons.update(mouse_pos, click)

    def _draw(self):
        visual_manager.draw_background()
        groups.buttons.draw(visual_manager.get_screen())

    def _teardown(self):
        for sprite in groups.all_sprites:
            sprite.kill()
