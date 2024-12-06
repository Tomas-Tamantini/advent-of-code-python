from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_patrol_area, parse_patrol_guard


def aoc_2024_d6(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 6, "Guard Gallivant")
    io_handler.output_writer.write_header(problem_id)
    yield from []
