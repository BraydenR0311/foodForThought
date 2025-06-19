import random

import pygame as pg

from .. import config


class AudioManager:
    def __init__(self):
        self.songs = list((config.AUDIO_DIR / "music").iterdir())

    def play_music(self):
        if not pg.mixer.music.get_busy():
            song = random.choice(self.songs)
            pg.mixer.music.load(song)
            pg.mixer.music.play()

    def play_sound(self, sound_file):
        sound = pg.mixer.Sound(sound_file)
        sound.play()
