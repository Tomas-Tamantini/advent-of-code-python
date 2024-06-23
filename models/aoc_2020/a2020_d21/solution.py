from models.common.io import IOHandler, Problem
from .parser import parse_foods
from .foods import Foods


def aoc_2020_d21(io_handler: IOHandler) -> None:
    problem_id = Problem(2020, 21, "Allergen Assessment")
    io_handler.output_writer.write_header(problem_id)
    foods = Foods(list(parse_foods(io_handler.input_reader)))
    num_times = sum(
        foods.num_times_ingredient_appears(ingredient)
        for ingredient in foods.ingredients_without_allergens()
    )
    print(f"Part 1: Number of times non-allergen ingredients appear is {num_times}")
    matches: dict[str, str] = foods.ingredients_with_allergens()
    canonical_dangerous_ingredients = ",".join(
        ingredient for ingredient in sorted(matches.keys(), key=matches.get)
    )
    print(
        f"Part 2: Canonical dangerous ingredient list is {canonical_dangerous_ingredients}"
    )
