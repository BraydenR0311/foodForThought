from typing import override

from .. import config
from .text import Text
from ..utils.utils import get_screen_rect
from .generic import Generic


class TypeTimer(Text):
    """Times and keeps track of wrongs."""

    containers = None

    def __init__(
        self,
        duration: int,
        current_tick: int,
        fontsize: int,
        color: str,
        bgcolor=None,
    ):
        super().__init__(str(duration), fontsize, color, bgcolor)
        self._duration = duration
        self._start = current_tick
        # Location of wrongs relative to center of timer.
        self.wrong_locs = [(-50, 100), (0, 100)]
        self.wrongs = []

        # Position sprite.
        self.rect.center = get_screen_rect().center
        self.rect.move_ip(get_screen_rect().width // 3, 0)

        self._done = False

    def is_done(self) -> bool:
        """Returns True if the timer has finished."""
        return self._done

    @override
    def kill(self):
        """Ensure timer sprite and all subcomponents have been killed."""
        super().kill()
        for wrong in self.wrongs:
            wrong.kill()

    def add_wrong(self):
        """When the user messes up typing, add an X below timer."""
        wrong = Generic(config.IMAGE_DIR / "x.png")
        # Position.
        wrong.rect.center = self.rect.center
        wrong.rect.move_ip(self.wrong_locs[len(self.wrongs)])

        self.wrongs.append(wrong)

    @override
    def update(self, elapsed: int, *args, **kwargs):
        """Needs elapsed from a clock object that keeps track of level time."""
        super().update()
        # Whole seconds that have passed since starting.
        passed = int(elapsed - self._start) // 1000
        # Count down in whole seconds.
        self._content = str(self._duration - passed)
        # Time is up.
        if passed > self._duration and not self._done:
            self._done = True
