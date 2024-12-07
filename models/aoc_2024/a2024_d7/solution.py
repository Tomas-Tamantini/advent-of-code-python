from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_equations


def aoc_2024_d7(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 7, "Bridge Repair")
    io_handler.output_writer.write_header(problem_id)
    yield from []
