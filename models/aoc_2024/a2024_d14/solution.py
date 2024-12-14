from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_security_robots


def aoc_2024_d14(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 14, "Restroom Redoubt")
    io_handler.output_writer.write_header(problem_id)
    yield from []
