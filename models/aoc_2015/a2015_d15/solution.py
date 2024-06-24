from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_cookie_properties
from .cookie import CookieRecipe


def aoc_2015_d15(io_handler: IOHandler) -> None:
    problem_id = Problem(2015, 15, "Science for Hungry People")
    io_handler.output_writer.write_header(problem_id)
    ingredients = list(parse_cookie_properties(io_handler.input_reader))
    recipe = CookieRecipe(ingredients, num_tablespoons=100)
    optimal_recipe = recipe.optimal_recipe()
    result = optimal_recipe.score()
    solution = ProblemSolution(
        problem_id,
        f"Score of optimal recipe without calories restriction {result}",
        result,
        part=1,
    )
    io_handler.set_solution(solution)
    optimal_diet_recipe = recipe.optimal_recipe(num_calories=500)
    result = optimal_diet_recipe.score()
    solution = ProblemSolution(
        problem_id,
        f"Score of optimal recipe with calories restriction {result}",
        result,
        part=2,
    )
    io_handler.set_solution(solution)
