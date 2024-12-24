from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_logic_gates


def aoc_2024_d24(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 24, "Crossed Wires")
    io_handler.output_writer.write_header(problem_id)
    yield from []
