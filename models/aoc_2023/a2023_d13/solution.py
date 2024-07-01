from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_mirrors


def aoc_2023_d13(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 13, "Point of Incidence")
    io_handler.output_writer.write_header(problem_id)
    yield from []
