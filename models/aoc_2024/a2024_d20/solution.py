from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_x


def aoc_2024_d20(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 20, "Race Condition")
    io_handler.output_writer.write_header(problem_id)
    yield from []
