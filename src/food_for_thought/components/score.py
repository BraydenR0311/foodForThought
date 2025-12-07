import pygame as pg

from .text import Text
from ..managers.visualmanager import VisualManager
import random

import logging

logger = logging.getLogger(__name__)

visual_manager = VisualManager()


class Score(Text):
    def __init__(self):
        self._value = 0.0
        super().__init__(self.get_text(), 20, "black")

    def update(self, *args, **kwargs):
        super().update()
        self._content = self.get_text()
        self.rect.topright = visual_manager.get_screen_rect().topright
        self.rect.move_ip(0, 30)

    def get_text(self):
        return f"Money made: ${self._value:.2f}"

    def get_value(self):
        return self._value

    def increase_random(self, value: int):
        if value == 0:
            return 0.0
        direction = random.choice([-1, 1])
        magnitude = random.random()
        earnings = value + direction * magnitude
        self._value += earnings
        return earnings
