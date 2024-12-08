from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_antenna_range


def aoc_2024_d8(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 8, "Resonant Collinearity")
    io_handler.output_writer.write_header(problem_id)
    yield from []
