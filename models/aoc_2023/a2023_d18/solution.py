from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_dig_plan


def aoc_2023_d18(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 18, "Lavaduct Lagoon")
    io_handler.output_writer.write_header(problem_id)
    yield from []
