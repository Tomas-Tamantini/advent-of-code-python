from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_initialization_sequence


def aoc_2023_d15(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 15, "Lens Library")
    io_handler.output_writer.write_header(problem_id)
    yield from []
