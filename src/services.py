import random
from pathlib import Path
import pygame as pg

def quotegen(quotes: dict) -> tuple[str, str]:
    """Returns a tuple of an author and one of their quotes.
    """
    
    author = random.choice(list(quotes.keys()))
    quote = random.choice(quotes[author])

    return author, quote

def quoteread(file: str | Path) -> dict[str, list]:
    """Read quotes.txt and return dictionary in the form of {author: quote}
    """

    quotes = {}
    author = None

    with open(file, 'r', encoding='utf-8') as infile:
        for line in infile:
            line = line.strip()
            # Empty lines separate author/quote blocks
            if not line:
                author = None
            # Found an author
            elif not author:
                author = line
                quotes[author] = []
            else:
                quotes[author].append(line)

    return quotes
