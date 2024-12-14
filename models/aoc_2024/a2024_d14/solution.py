from math import prod
from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .guarded_bathroom import GuardedBathroom
from .parser import parse_security_robots


def aoc_2024_d14(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 14, "Restroom Redoubt")
    io_handler.output_writer.write_header(problem_id)
    guards = parse_security_robots(io_handler.input_reader)
    bathroom = GuardedBathroom(width=101, height=103)
    num_per_quadrant = bathroom.num_guards_per_quadrant(guards, time=100)
    result = prod(num_per_quadrant)
    yield ProblemSolution(problem_id, f"The safety factor is {result}", result, part=1)
