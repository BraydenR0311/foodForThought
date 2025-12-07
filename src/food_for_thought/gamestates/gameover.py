from typing import override

import pygame as pg
from .. import groups

from .gamestate import GameState
from ..gamestates.statekey import StateKey

from ..components.typeui import TypeUI
from ..components.ticket import Ticket, TicketIngredient
from ..components.levelclock import LevelClock
from ..components.text import Text
from ..managers.gamestatemanager import GameStateManager
from ..managers.visualmanager import VisualManager
from ..managers.audiomanager import AudioManager

import logging

logger = logging.getLogger(__name__)

gamestate_manager = GameStateManager()
visual_manager = VisualManager()
audio_manager = AudioManager()


class GameOver(GameState):
    def __init__(self) -> None:
        super().__init__(StateKey.GAME_OVER)

    @override
    def _setup(self):
        score = self.data["score"]
        self.score_text = Text(f"you made ${score.get_value():.2f}! Wow!", 50)
        self.score_text.rect.center = visual_manager.get_screen_rect().center

        self.space_text = Text("(Press Space to return to main menu)", 30)
        self.space_text.rect.midtop = self.score_text.rect.midbottom
        self.space_text.rect.move_ip(0, 10)

    @override
    def run(self):
        events = self.data["events"]

        for event in events:
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                gamestate_manager.goto(StateKey.MAIN_MENU, teardown=True)

        self._draw()

    @override
    def _update(self):
        pass

    @override
    def _draw(self):
        visual_manager.draw_background()
        visual_manager.draw(
            groups.texts,
        )

    @override
    def _teardown(self):
        for sprite in groups.all_sprites.sprites():
            sprite.kill()
