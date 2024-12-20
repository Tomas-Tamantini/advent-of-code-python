from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .parser import parse_calories


def aoc_2022_d1(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2022, 1, "Calorie Counting")
    io_handler.output_writer.write_header(problem_id)
    calories_by_elf = [
        sum(calories) for calories in parse_calories(io_handler.input_reader)
    ]
    sorted_calories = sorted(calories_by_elf)
    max_calories = sorted_calories[-1]
    yield ProblemSolution(
        problem_id, f"Maximum calories is {max_calories}", part=1, result=max_calories
    )

    top_3_calories = sum(sorted_calories[-3:])
    yield ProblemSolution(
        problem_id,
        f"Sum of top 3 calories is {top_3_calories}",
        part=2,
        result=top_3_calories,
    )
