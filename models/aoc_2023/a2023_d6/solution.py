from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_boat_races


def aoc_2023_d6(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 6, "Wait For It")
    io_handler.output_writer.write_header(problem_id)
    yield from []
