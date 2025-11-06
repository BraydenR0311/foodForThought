import pygame as pg

from .text import Text
from ..managers.visualmanager import VisualManager


visual_manager = VisualManager()


class LevelClock(Text):
    """Manages 9 to 5 shift. Records time and updates on-screen clock."""

    SECS_IN_HOUR = 15
    containers = None

    def __init__(self):
        # Working day starts at 9 AM.
        self.text = "9:00"
        super().__init__(self.text, 20, "black")
        self.hour = 9
        self.tick = False  # The clock is currently changing.
        self.start_time = pg.time.get_ticks()
        self.paused_elapsed = 0
        self.pause_start = 0
        self.has_been_paused = False

    def update(self, *args, **kwargs):
        self.update_text()

    def start(self):
        if self.has_been_paused:
            self.paused_elapsed += pg.time.get_ticks() - self.pause_start

    def pause(self):
        if not self.has_been_paused:
            self.has_been_paused = True
        self.pause_start = pg.time.get_ticks()

    def get_elapsed(self) -> int:
        return pg.time.get_ticks() - self.start_time - self.paused_elapsed

    def update_text(self):
        secs = self.get_elapsed() // 1000
        if self.hour > 12:
            self.hour -= 12
        if (secs % self.SECS_IN_HOUR == 0) and secs > 0 and not self.tick:
            self.tick = not self.tick
            self.hour += 1
        if (not secs % self.SECS_IN_HOUR == 0) and self.tick:
            self.tick = not self.tick
        self.text = str(self.hour) + ":00"
        # When text, make sure it's positioned correctly.
        self.rect.topright = visual_manager.get_screen_rect().topright
