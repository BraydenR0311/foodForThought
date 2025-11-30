import pygame as pg
from .type_timer import TypeTimer
from ..components.text import Text
from ..managers.visualmanager import VisualManager
import logging

logger = logging.getLogger(__name__)

visual_manager = VisualManager()


class TypeUI:
    def __init__(self, quote_chunk: str, level_elapsed: int, fontsize: int) -> None:
        self._text = Text(
            quote_chunk,
            fontsize,
            "black",
            midbottom=visual_manager.get_screen_rect().move(0, -20).midbottom,
        )
        # Time is based on number of words and then some.
        self._timer = TypeTimer(
            len(self._text.get_content().split()) + 3, level_elapsed, 15, "black"
        )
        # User's typed text that will mask original text.
        self._user_input = Text(
            "",
            fontsize,
            "green",
            topleft=self._text.rect.topleft,
        )
        self._user_input_buffer = ""
        self._is_erring = False
        self._misses = 0

    def times_up(self) -> bool:
        """Timer is done."""
        return self._timer.is_done()

    def is_written(self) -> bool:
        """User has successfully written text."""
        return self._text.get_content() == self._user_input.get_content()

    def num_misses(self) -> int:
        """Return number of misses"""
        return self._misses

    def kill(self) -> None:
        "Remove sprites from screen."
        self._user_input.kill()
        self._text.kill()
        self._timer.kill()

    def update(self, elapsed) -> None:
        """Need elapsed time from an object that manages level time."""
        self._timer.update(elapsed)
        self._text.update()
        self._user_input.update()

    def handle_input(self, events: list[pg.event.Event]) -> None:
        """Handle input from list of events from pg.event.get()"""
        # Enforce whether or not user input is matching text.
        # self._handle_erring()

        for event in events:
            # User types something.
            if event.type == pg.TEXTINPUT:
                if not event.text.isascii():
                    continue
                if not self._is_erring:
                    self._user_input_buffer += event.text
                    if not self._text.get_content().startswith(self._user_input_buffer):
                        self._is_erring = True
                        self._text.change_color("red")
                        self._user_input.change_color("red")
                        self._misses += 1
                        self._timer.add_wrong()
                    else:
                        self._user_input.replace_text(self._user_input_buffer)

            # User presses backspace.
            elif event.type == pg.KEYDOWN and event.key == pg.K_BACKSPACE:
                # Remove a character.
                if self._is_erring:
                    self._is_erring = False
                    self._user_input_buffer = self._user_input_buffer[:-1]
                    self._user_input.change_color("green")
                    self._text.change_color("black")
