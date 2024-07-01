from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_hailstones


def aoc_2023_d24(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 24, "Never Tell Me The Odds")
    io_handler.output_writer.write_header(problem_id)
    yield from []
