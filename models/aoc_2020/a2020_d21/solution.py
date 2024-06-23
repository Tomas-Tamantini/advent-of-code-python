from models.common.io import IOHandler, Problem, ProblemSolution
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
    solution = ProblemSolution(
        problem_id,
        f"Number of times non-allergen ingredients appear is {num_times}",
        part=1,
    )
    io_handler.set_solution(solution)
    matches: dict[str, str] = foods.ingredients_with_allergens()
    canonical_dangerous_ingredients = ",".join(
        ingredient for ingredient in sorted(matches.keys(), key=matches.get)
    )
    solution = ProblemSolution(
        problem_id,
        f"Canonical dangerous ingredient list is {canonical_dangerous_ingredients}",
        part=2,
    )
    io_handler.set_solution(solution)
