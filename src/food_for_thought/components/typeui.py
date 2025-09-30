import pygame as pg
from ..components.timer import Timer
from ..components.text import Text


class TypeUI:
    def __init__(self, quote_part: str, current_tick: int, fontsize: int) -> None:
        self._text = Text(quote_part, fontsize, "black")
        self._timer = Timer(
            len(self._text.get_content().split()) + 3, current_tick, 15, "black"
        )
        self._user_input = Text("", fontsize, "green")
        self._is_erring = False
        self._misses = 0

    def times_up(self) -> bool:
        return self._timer.is_done()

    def is_written(self) -> bool:
        self._text.get_content() == self._user_input.get_content()

    def get_misses(self) -> int:
        """Return number of misses"""
        return self._misses

    def kill(self) -> None:
        "Remove sprites from screen."
        self._user_input.kill()
        self._text.kill()
        self._timer.kill()

    def update(self, elapsed) -> None:
        self._timer.update(elapsed)

    def handle_input(self, events: list[pg.Event]) -> None:
        """Handle input from list of events from pg.event.get()"""
        # Enforce whether or not user input is matching text.
        self._handle_erring()

        for event in events:
            # User types something.
            if event.type == pg.TEXTINPUT:
                if event.text.isascii() and not self._is_erring:
                    # Add new character.
                    self._user_input.add_char(event.text)
            # User presses backspace.
            elif event.type == pg.KEYDOWN and event.key == pg.K_BACKSPACE:
                # Remove a character.
                self._user_input.remove_char()

    def _handle_erring(self) -> None:
        """Update status of whether or not user input is wrong."""
        # User input does not line up with text.
        if not self._text.get_content().startswith(self._user_input.get_content()):
            # If previously not erring...
            if not self._is_erring:
                self._misses += 1
                self._text.change_color("red")
                # Display red check under timer.
                self._timer.add_wrong()
            self._is_erring = True
        else:
            # If previously erring...
            if self._is_erring:
                self._text.change_color("green")
            self._is_erring = False
