from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_gear_ratios


def aoc_2023_d3(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 3, "Gear Ratios")
    io_handler.output_writer.write_header(problem_id)
    yield from []
