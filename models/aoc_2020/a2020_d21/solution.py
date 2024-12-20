from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .foods import Foods
from .parser import parse_foods


def aoc_2020_d21(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2020, 21, "Allergen Assessment")
    io_handler.output_writer.write_header(problem_id)
    foods = Foods(list(parse_foods(io_handler.input_reader)))
    num_times = sum(
        foods.num_times_ingredient_appears(ingredient)
        for ingredient in foods.ingredients_without_allergens()
    )
    yield ProblemSolution(
        problem_id,
        f"Number of times non-allergen ingredients appear is {num_times}",
        part=1,
        result=num_times,
    )

    matches: dict[str, str] = foods.ingredients_with_allergens()
    canonical_dangerous_ingredients = ",".join(
        ingredient for ingredient in sorted(matches.keys(), key=matches.get)
    )
    yield ProblemSolution(
        problem_id,
        f"Canonical dangerous ingredient list is {canonical_dangerous_ingredients}",
        part=2,
        result=canonical_dangerous_ingredients,
    )
