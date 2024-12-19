from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .build_design import num_ways_to_make_design
from .parser import parse_available_patterns, parse_desired_designs


def aoc_2024_d19(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 19, "Linen Layout")
    io_handler.output_writer.write_header(problem_id)
    patterns = list(parse_available_patterns(io_handler.input_reader))
    designs = list(parse_desired_designs(io_handler.input_reader))

    num_ways = 0
    num_possible_designs = 0

    for design in designs:
        increment = num_ways_to_make_design(design, patterns)
        num_ways += increment
        num_possible_designs += increment > 0

    yield ProblemSolution(
        problem_id,
        f"The number of possible designs is {num_possible_designs}",
        result=num_possible_designs,
        part=1,
    )

    yield ProblemSolution(
        problem_id,
        f"The number of ways to make the desired designs is {num_ways}",
        result=num_ways,
        part=2,
    )
