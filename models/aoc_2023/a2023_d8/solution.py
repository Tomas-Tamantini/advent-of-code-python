from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_node_network


def aoc_2023_d8(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 8, "Haunted Wasteland")
    io_handler.output_writer.write_header(problem_id)
    yield from []
