import pygame as pg

from paths import *
from src.components.text import Text
from src.utils.utils import get_screen_rect

class ShiftClock(Text):
    """Manages 9 to 5 shift. Records time and updates on-screen clock."""
    SECS_IN_HOUR = 15
    containers = None

    def __init__(self, fontsize, color, bgcolor=None):
        super().__init__(fontsize, color, bgcolor)
        # Working day starts at 9 AM.
        self.text = '9:00'
        self.hour = 9
        self.tick = False # The clock is currently changing.
        self.start_time = 0
        self.paused_time = 0
        self.pause_start = 0
        self.is_running = False

        self.image = None
        self.rect = None

    def update(self, *args, **kwargs):
        self.update_text()

    def start(self):
        if not self.start_time:
            self.start_time = pg.time.get_ticks()
        if not self.is_running:
            self.is_running = True
            if self.pause_start:
                self.paused_time += pg.time.get_ticks() - self.pause_start

    def pause(self):
        if self.is_running:
            self.pause_start = pg.time.get_ticks()
            self.is_running = False
    
    def get_elapsed(self):
        return pg.time.get_ticks() - self.start_time - self.paused_time

    def update_text(self):
        secs = self.get_elapsed() // 1000
        if self.hour > 12:
            self.hour -= 12
        if ((secs % self.SECS_IN_HOUR == 0) and
            secs > 0 and
            not self.tick):
            self.tick = not self.tick
            self.hour += 1
        if (not secs % self.SECS_IN_HOUR == 0) and self.tick:
            self.tick = not self.tick
        self.text = str(self.hour) + ':00'
        self.image = self.font.render(
            self.text, 1, self.color, self.bgcolor
        )
        self.rect = self.image.get_rect()
        # When text, make sure it's positioned correctly.
        self.rect.topright = get_screen_rect().topright
