from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_claw_machines


def aoc_2024_d13(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 13, "Claw Contraption")
    io_handler.output_writer.write_header(problem_id)
    yield from []
