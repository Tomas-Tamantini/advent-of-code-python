from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_3_bit_program


def aoc_2024_d17(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 17, "Chronospatial Computer")
    io_handler.output_writer.write_header(problem_id)
    yield from []
