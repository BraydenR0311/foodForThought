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
    image_path: Path


MENU = {
    "burger": Dish(
        "burger",
        [
            Ingredient("bun", TileType.cutting_board, FOOD_DIR / "bun.png"),
            Ingredient("patty", TileType.oven, FOOD_DIR / "patty.png"),
            Ingredient("cheese", TileType.cutting_board, FOOD_DIR / "cheese.png"),
        ],
        FOOD_DIR / "burger.png",
    ),
    "taco": Dish(
        "taco",
        [
            Ingredient("shell", TileType.cutting_board, FOOD_DIR / "shell.png"),
            Ingredient("tomato", TileType.cutting_board, FOOD_DIR / "tomato.png"),
            Ingredient("beef", TileType.oven, FOOD_DIR / "beef.png"),
        ],
        FOOD_DIR / "taco.png",
    ),
}
