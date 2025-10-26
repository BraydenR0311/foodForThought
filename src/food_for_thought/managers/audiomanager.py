import random

import pygame as pg

from ..config import SOUND_DIR, MUSIC_DIR
import random


class AudioManager:
    _instance = None
    _initialized = False

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if AudioManager._initialized:
            return
        pg.mixer.init()
        AudioManager._initialized = True
        self.songs = [MUSIC_DIR / f for f in MUSIC_DIR.iterdir()]
        self.queue = self._get_random_music_queue()
        self.current_track = None
        self.sounds = {
            "sizzle": pg.mixer.Sound(SOUND_DIR / "sizzle.ogg"),
            "chop": pg.mixer.Sound(SOUND_DIR / "chop.ogg"),
            "click_up": pg.mixer.Sound(SOUND_DIR / "click_up.opus"),
            "click_down": pg.mixer.Sound(SOUND_DIR / "click_down.opus"),
        }

    def play_music(self):
        if pg.mixer.music.get_busy():
            return
        if not self.queue:
            self.queue = self._get_random_music_queue()
        self.current_track = self.queue.pop()
        pg.mixer.music.load(self.current_track)
        pg.mixer.music.play()

    def play_sound(self, sound_name):
        self.sounds[sound_name].play()

    def stop_sound(self, sound_name):
        self.sounds[sound_name].stop()

    def _get_random_music_queue(self) -> list:
        queue = self.songs.copy()
        random.shuffle(queue)
        return queue
