from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_workflows


def aoc_2023_d19(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 19, "Aplenty")
    io_handler.output_writer.write_header(problem_id)
    yield from []
