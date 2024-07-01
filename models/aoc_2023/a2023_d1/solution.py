from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .digit_finder import find_digits


def aoc_2023_d1(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 1, "Trebuchet?!")
    io_handler.output_writer.write_header(problem_id)
    sequences = list(io_handler.input_reader.read_stripped_lines())
    total_sum = 0
    for sequence in sequences:
        digits = list(find_digits(sequence))
        total_sum += digits[0].value * 10 + digits[-1].value
    yield ProblemSolution(
        problem_id,
        solution_text=f"The sum of calibation values is {total_sum}",
        result=total_sum,
    )
    yield from []
