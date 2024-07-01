from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_pipe_maze


def aoc_2023_d10(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 10, "Pipe Maze")
    io_handler.output_writer.write_header(problem_id)
    yield from []
