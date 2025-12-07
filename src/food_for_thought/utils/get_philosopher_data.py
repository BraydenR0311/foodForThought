# Data gathered from https://philosophersapi.com/.
# All credit goes to Brad Gayman for philosopher data.
# %%
import json
import random
import requests
from yarl import URL
from pathlib import Path
from unidecode import unidecode

ROOT_URL = URL("https://philosophersapi.com")
QUOTE_URL = ROOT_URL / "api/quotes"
PHILOSOPHER_URL = ROOT_URL / "api/philosophers"

response = requests.get(QUOTE_URL)
data = response.json() if response.status_code == 200 else []
# %%
quotes = []
while data:
    # Take a random quote and remove from list to prevent duplicates.
    data.remove(quote_data := random.choice(data))
    author_id = quote_data["philosopher"]["id"]
    quote = unidecode(quote_data["quote"])

    # Get philosopher data from unique id.
    response = requests.get(PHILOSOPHER_URL / author_id)
    author_data = response.json() if response.status_code == 200 else []
    if not author_data:
        continue

    # Remove non-ascii characters (ie. with accents or slashes in them).
    author = unidecode(author_data["name"])
    # Strip the fist '/' so we can concatenate to ROOT_URL later.
    image = author_data["images"]["faceImages"]["face250x250"].lstrip("/")

    # Quote skipped of number of characters exceeds this.
    if len(quote) > 250:
        continue

    quotes.append({"author": author, "id": author_id, "quote": quote, "image": image})

    print(quotes[-1])
    print()

# %%
with open("quotes.json", "w") as outfile:
    json.dump(quotes, outfile, indent=4)
# %%
IMAGE_DIR = Path("faces")
if not IMAGE_DIR.exists():
    IMAGE_DIR.mkdir()

unique_authors = set(quote["author"] for quote in quotes)
for author in unique_authors:
    # Find author's matching data.
    for quote in quotes:
        if quote["author"] == author:
            break
    response = requests.get(ROOT_URL / quote["image"])
    jpg_data = response.content if response.status_code == 200 else []
    if jpg_data:
        jpg_name = quote["id"] + ".jpg"
        with open(IMAGE_DIR / jpg_name, "wb") as outfile:
            outfile.write(jpg_data)
