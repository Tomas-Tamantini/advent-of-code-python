from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_forest_map


def aoc_2023_d23(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 23, "A Long Walk")
    io_handler.output_writer.write_header(problem_id)
    yield from []
