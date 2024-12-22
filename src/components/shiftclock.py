import time

import pygame as pg

from constants import *
from paths import *
from src.components.text import Text

class ShiftClock(Text):
    """
    Manages 9 to 5 shift.

    Parameters:
    ---
    - secs: pg.time.get_ticks // 1000
    """

    containers = None

    def __init__(self, text, font, fontsize, color, bgcolor=None):
        super().__init__(text, font, fontsize, color, bgcolor)
        self.hour = 9
        self.secs = 0
        self.tick = False
        self.starttime = 0

    def update(self):

        self.secs = int(time.time() - self.starttime)
        self.change_time()
    
    def start_time(self):
        self.starttime = time.time()




    def change_time(self):
        if self.hour > 12:
            self.hour -= 12
        if ((self.secs % 30 == 0) and
            self.secs > 0 and
            not self.tick):
            self.tick = not self.tick
            self.hour += 1
        if (not self.secs % 30 == 0) and self.tick:
            self.tick = not self.tick
        self.text = str(self.hour) + ':00'
        self.image = self.font.render(self.text, 1,
                                      self.color, self.bgcolor)
        self.rect = self.image.get_rect()
        self.rect.topright = SCREEN_RECT.topright