import pygame as pg

from .. import config
from ..managers.audiomanager import AudioManager

audio_manager = AudioManager()


class Button(pg.sprite.Sprite):
    IMAGE_PATHS = {
        "play": config.IMAGE_DIR / "buttons" / "play.png",
        "quit": config.IMAGE_DIR / "buttons" / "quit.png",
    }

    containers = None
    images = {}

    def __init__(self, kind: str, center_loc: tuple[int, int]):
        super().__init__(self.containers)
        self.kind = kind
        self.image = self.images[self.kind]
        self.rect = self.image.get_rect()
        self.rect.center = center_loc
        self.clicked = False
        self.armed = False
        self.activated = False

    def update(self, *args, **kwargs):
        mouse_pos = pg.mouse.get_pos()
        click, _, _ = pg.mouse.get_pressed()

        # If previously activated, deactivate.
        if self.activated:
            self.activated = False

        # Mouse hovering over self.
        armed = self.rect.collidepoint(mouse_pos)

        # Nothing done to self.
        if not armed and not click:
            if self.clicked:
                audio_manager.play_sound("click_up")

            self.armed = False
            self.unarm()
            self.clicked = False

        # Mouse is now hovering.
        if armed and not self.armed:
            self.armed = True
            self.arm()

        # Hovering and now left click held.
        if armed and click and not self.clicked:
            self.click()
            self.clicked = True

        # Activate self.
        if armed and not click and self.clicked:
            self.clicked = False
            self.activated = True
            audio_manager.play_sound("click_up")

    def arm(self):
        self.image = pg.transform.hsl(self.image, lightness=-0.2)

    def unarm(self):
        self.image = self.images[self.kind]

    def click(self):
        self.image = pg.transform.hsl(self.image, lightness=-0.3)
        audio_manager.play_sound("click_down")
