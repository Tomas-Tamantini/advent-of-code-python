from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_cube_games


def aoc_2023_d2(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 2, "Cube Conundrum")
    io_handler.output_writer.write_header(problem_id)
    yield from []
