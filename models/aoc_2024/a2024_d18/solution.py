from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_byte_positions


def aoc_2024_d18(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 18, "RAM Run")
    io_handler.output_writer.write_header(problem_id)
    yield from []
