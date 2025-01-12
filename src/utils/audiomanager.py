import random

import pygame as pg

from paths import *
from src.config import Config
# TODO: Get rid of this
class AudioManager():
    def __init__(self):
        self.songs = list((AUDIO_DIR / 'music').iterdir())
    
    def play_music(self):
        if not pg.mixer.music.get_busy():
            song = random.choice(self.songs)
            pg.mixer.music.load(song)
            pg.mixer.music.play()
    
    def play_sound(self, sound_file):
        sound = pg.mixer.Sound(sound_file)
        sound.play()