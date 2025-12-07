import pygame as pg

from .text import Text
from ..managers.visualmanager import VisualManager
from ..managers.audiomanager import AudioManager
import random

import logging

logger = logging.getLogger(__name__)

visual_manager = VisualManager()
audio_manager = AudioManager()


class ScorePopup(Text):
    def __init__(self, value: float, table):
        self._value = value
        super().__init__(self.get_text(), 20, "green")

        self._table = table
        self._ttl = 2000
        self._speed = 100
        self._start_elapsed = None
        self.rect.center = self._table.rect.move(0, -20).center

        audio_manager.play_sound("cash_register")

    def update(self, elapsed, dt, *args, **kwargs):
        if not self._start_elapsed:
            self._start_elapsed = elapsed

        lifetime = (elapsed - self._start_elapsed) / self._ttl
        alpha_value = pg.math.lerp(255, 0, lifetime)
        self.image.set_alpha(int(alpha_value))

        logger.debug(f"{alpha_value=}")

        pixels_up_this_frame = -self._speed * dt
        logger.debug(f"{pixels_up_this_frame=}")
        self.rect.move_ip(0, pixels_up_this_frame)

        if lifetime >= 1:
            self.kill()

    def get_text(self):
        return f"+${self._value:.2f}"
