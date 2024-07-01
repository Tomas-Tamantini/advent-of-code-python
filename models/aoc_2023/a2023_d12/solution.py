from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_damaged_springs


def aoc_2023_d12(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 12, "Hot Springs")
    io_handler.output_writer.write_header(problem_id)
    yield from []
