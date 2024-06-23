from models.common.io import IOHandler, Problem, ProblemSolution
from .hot_chocolate import HotChocolateRecipeScores


def aoc_2018_d14(io_handler: IOHandler) -> None:
    problem_id = Problem(2018, 14, "Chocolate Charts")
    io_handler.output_writer.write_header(problem_id)
    num_steps = int(io_handler.input_reader.read())
    recipe_scores = HotChocolateRecipeScores(first_score=3, second_score=7)
    score_generator = recipe_scores.generate_scores()
    first_scores = [next(score_generator) for _ in range(num_steps + 10)]
    last_ten_scores = "".join(map(str, first_scores[num_steps : num_steps + 10]))
    solution = ProblemSolution(
        problem_id, f"Scores of next 10 recipes: {last_ten_scores}", part=1
    )
    io_handler.set_solution(solution)
    first_occurrence = recipe_scores.first_occurrence_of_subsequence(
        tuple(map(int, str(num_steps))), io_handler.progress_bar
    )
    solution = ProblemSolution(
        problem_id,
        f"Number of recipes to the left of the score sequence: {first_occurrence}",
        part=2,
    )
    io_handler.set_solution(solution)
