from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_connections


def aoc_2024_d23(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 23, "LAN Party")
    io_handler.output_writer.write_header(problem_id)
    yield from []
