from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_available_patterns


def aoc_2024_d19(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 19, "Linen Layout")
    io_handler.output_writer.write_header(problem_id)
    yield from []
