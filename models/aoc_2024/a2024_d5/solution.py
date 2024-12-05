from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_page_ordering_rules


def aoc_2024_d5(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 5, "Print Queue")
    io_handler.output_writer.write_header(problem_id)
    yield from []
