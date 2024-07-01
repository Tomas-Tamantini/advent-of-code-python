from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_seeds_and_maps


def aoc_2023_d5(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 5, "If You Give A Seed A Fertilizer")
    io_handler.output_writer.write_header(problem_id)
    yield from []
