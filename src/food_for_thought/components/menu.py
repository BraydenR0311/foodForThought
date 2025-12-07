from dataclasses import dataclass
from .tile import TileType
from pathlib import Path
from ..config import FOOD_DIR


@dataclass(frozen=True)
class Ingredient:
    name: str
    appliance: TileType
    image_path: Path


@dataclass(frozen=True)
class Dish:
    name: str
    ingredients: list[Ingredient]


BEEF = Ingredient("beef", TileType.grill, FOOD_DIR / "beef.png")
TOMATO = Ingredient("tomato", TileType.cutting_board, FOOD_DIR / "tomato.png")
CHEESE = Ingredient("cheese", TileType.cutting_board, FOOD_DIR / "cheese.png")
LETTUCE = Ingredient("lettuce", TileType.cutting_board, FOOD_DIR / "lettuce.png")
NOODLES = Ingredient("noodles", TileType.pot, FOOD_DIR / "noodles.png")
HAM = Ingredient("ham", TileType.grill, FOOD_DIR / "ham.png")
BREAD = Ingredient("bread", TileType.cutting_board, FOOD_DIR / "bread.png")
EGG = Ingredient("egg", TileType.grill, FOOD_DIR / "egg.png")
POTATO = Ingredient("potato", TileType.cutting_board, FOOD_DIR / "potato.png")
FRIES = Ingredient("fries", TileType.fryer, FOOD_DIR / "fries.png")
FRIED_FISH = Ingredient("fried_fish", TileType.fryer, FOOD_DIR / "fish.png")
BAKED_FISH = Ingredient("baked_fish", TileType.oven, FOOD_DIR / "fish.png")


MENU = {
    "burger": Dish(
        "Burger",
        [BEEF, TOMATO, CHEESE],
    ),
    "beef_taco": Dish(
        "Beef Taco",
        [BEEF, TOMATO, LETTUCE],
    ),
    "fish_taco": Dish(
        "Fish Taco",
        [BAKED_FISH, TOMATO, LETTUCE],
    ),
    "ham_sandwich": Dish(
        "Ham Sandwich",
        [BREAD, HAM, CHEESE],
    ),
    "spaghetti": Dish(
        "Spaghetti",
        [NOODLES, TOMATO, BEEF],
    ),
    "breakfast_sandwich": Dish(
        "Breakfast Sandwich",
        [BREAD, EGG, CHEESE],
    ),
    "ramen": Dish(
        "Ramen",
        [NOODLES, HAM, EGG],
    ),
    "fish_and_chips": Dish(
        "Fish and Chips",
        [POTATO, FRIES, FRIED_FISH],
    ),
}
