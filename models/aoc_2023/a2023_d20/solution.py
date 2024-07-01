from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_module_network


def aoc_2023_d20(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 20, "Pulse Propagation")
    io_handler.output_writer.write_header(problem_id)
    yield from []
