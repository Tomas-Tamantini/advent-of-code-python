from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution
from .pseudo_random import next_pseudo_random


def aoc_2024_d22(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 22, "Monkey Market")
    io_handler.output_writer.write_header(problem_id)
    secret_numbers = [int(num) for num in io_handler.input_reader.read_stripped_lines()]

    total = 0
    for n in secret_numbers:
        current = n
        for i in range(2000):
            current = next_pseudo_random(current)
        total += current

    yield ProblemSolution(
        problem_id, f"The sum of generated numbers is {total}", result=total, part=1
    )
