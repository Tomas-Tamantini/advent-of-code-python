from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_warehouse_robot_moves


def aoc_2024_d15(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 15, "Warehouse Woes")
    io_handler.output_writer.write_header(problem_id)
    yield from []
