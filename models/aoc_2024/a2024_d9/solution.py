from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_disk


def aoc_2024_d9(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 9, "Disk Fragmenter")
    io_handler.output_writer.write_header(problem_id)
    yield from []
