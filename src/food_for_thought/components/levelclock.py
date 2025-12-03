import pygame as pg

from .text import Text
from ..managers.visualmanager import VisualManager
from .. import groups
import logging

logger = logging.getLogger()

visual_manager = VisualManager()


class LevelClock(Text):
    """Manages 9 to 5 shift. Records time and updates on-screen clock."""

    SECS_IN_HOUR = 15
    containers = (groups.texts, groups.all_sprites)

    def __init__(self):
        # Working day starts at 9 AM.
        super().__init__("Time: 9:00", 20, "black")
        self.hour = 9
        self.tick = False  # The clock is currently changing.
        self.start_time = pg.time.get_ticks()
        self.paused_elapsed = 0
        self.pause_start = 0
        self.has_been_paused = False

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
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
            self.tick = True
            self.hour += 1
            self._content = "Time: " + str(self.hour) + ":00"
            logger.debug("levelclock text: %s", self._content)

        if (not secs % self.SECS_IN_HOUR == 0) and self.tick:
            self.tick = False
        # When text, make sure it's positioned correctly.
        self.rect = self.image.get_rect()
        self.rect.topright = visual_manager.get_screen_rect().topright
