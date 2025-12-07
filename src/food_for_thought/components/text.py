import random
from typing import override

import pygame as pg

from .. import config
from ..common import QUOTE_DATA
import logging
from .. import groups
from .generic import Generic

logger = logging.getLogger(__name__)


class Text(pg.sprite.Sprite):
    """Simple text that can be rendered and acts like a sprite."""

    containers = (groups.texts, groups.all_sprites)

    def __init__(
        self,
        content: str,
        fontsize: int,
        color: str = "black",
        bgcolor=None,
        **rect_kwargs,
    ) -> None:
        super().__init__(self.containers)
        self._content = content
        self._font = pg.font.Font(config.DEFAULT_FONT, fontsize)
        self._color = color
        self._bgcolor = bgcolor

        self.image = self._font.render(self._content, True, self._color, self._bgcolor)
        self.rect = self.image.get_rect(**rect_kwargs)

    @override
    def update(self, *args, **kwargs):
        self.image = self._font.render(self._content, True, self._color, self._bgcolor)

    def get_content(self) -> str:
        """Return string content."""
        return self._content

    def change_color(self, new_color: str) -> None:
        """Update color in place."""
        self._color = new_color

    def replace_text(self, text: str) -> None:
        self._content = text

    def append_char(self, char: str):
        """Add a single character to the end of the string."""
        if len(char) > 1:
            raise ValueError("Char must be a string with length == 1.")
        self._content += char

    def backspace(self) -> None:
        """Remove number of letters from the end"""
        self._content = self._content[:-1]


class Quote:
    """Contains a quote separated by quote parts."""

    def __init__(self) -> None:
        # TODO: Author image
        # Get random quote data.
        data = random.choice(QUOTE_DATA)
        self._author = data["author"]
        self._lastname = self._author.split(" ")[-1]
        self._content = data["quote"].replace("\n", " ")
        self._image_path = config.FACES_DIR / f"{data['id']}.jpg"

        self._chunks = self._split_quote(self._content)

    def __len__(self) -> int:
        return len(self._chunks)

    def get_content(self) -> str:
        """Returns the entire quote, regardless if any have been popped."""
        return self._content

    def show_author_image(self, size, **rect_kwargs):
        return Generic(self._image_path, size, **rect_kwargs)

    def pop(self) -> str | None:
        """Pop the first quote part. Returns None if empty."""
        if not self._chunks:
            return None
        chunk = self._chunks.pop(0)
        return chunk

    @staticmethod
    def _split_quote(quote):
        """Helper method to split the quote into even chunks."""
        quote = quote.split()
        chunk_len = len(quote) // 3

        first = " ".join(quote[:chunk_len])
        second = " ".join(quote[chunk_len : 2 * chunk_len])
        third = " ".join(quote[2 * chunk_len :])

        chunks = [first, second, third]

        return chunks
