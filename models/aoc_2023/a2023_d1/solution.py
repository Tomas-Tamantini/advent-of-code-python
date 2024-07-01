from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution


def aoc_2023_d1(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 1, "Trebuchet?!")
    io_handler.output_writer.write_header(problem_id)
    yield from []
