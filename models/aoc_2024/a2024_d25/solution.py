from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_locks


def aoc_2024_d25(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 25, "Code Chronicle")
    io_handler.output_writer.write_header(problem_id)
    yield from []
