from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_camel_card_hands


def aoc_2023_d7(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 7, "Camel Cards")
    io_handler.output_writer.write_header(problem_id)
    yield from []
