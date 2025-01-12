import time

import pygame as pg

from paths import *
from src.components.text import Text
from src.utils.utils import get_screen_rect
from src.components.status import Status

class Timer(Text):
    """Times and keeps track of wrongs."""
    containers = None

    def __init__(self, length, font, fontsize, color, bgcolor=None):
        super().__init__(length, font, fontsize, color, bgcolor)
        self.length = length
        self.rect.center = get_screen_rect().center
        self.rect.move_ip(get_screen_rect().width // 3, 0)
        self.start = int(time.time())
    # Location of wrongs relative to center of timer.
        self.wrong_locs = [(-50, 100), (0, 100)]
        self.wrongs = []

    def add_wrong(self):
        """When the user messes up typing, add an X below timer."""
        wrong = Status(False)
        # Position.
        wrong.rect.center = self.rect.center
        wrong.rect.move_ip(self.wrong_locs[len(self.wrongs)])

        self.wrongs.append(wrong)

    def update(self, *args, **kwargs):
        now = int(time.time())
        passed = now - self.start
        self.text = str(self.length - passed)
        self.image = self.font.render(self.text, 1, self.color, self.bgcolor)