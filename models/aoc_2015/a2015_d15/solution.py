from models.common.io import InputReader
from .parser import parse_cookie_properties
from .cookie import CookieRecipe


def aoc_2015_d15(input_reader: InputReader, **_) -> None:
    print("--- AOC 2015 - Day 15: Science for Hungry People ---")
    ingredients = list(parse_cookie_properties(input_reader))
    recipe = CookieRecipe(ingredients, num_tablespoons=100)
    optimal_recipe = recipe.optimal_recipe()
    print(
        f"Part 1: Score of optimal recipe without calories restriction {optimal_recipe.score()}"
    )
    optimal_diet_recipe = recipe.optimal_recipe(num_calories=500)
    print(
        f"Part 2: Score of optimal recipe with calories restriction {optimal_diet_recipe.score()}"
    )
