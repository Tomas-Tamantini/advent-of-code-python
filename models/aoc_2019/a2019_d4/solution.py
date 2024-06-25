from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .valid_passwords import (
    digits_are_increasing,
    two_adjacent_digits_are_the_same,
    at_least_one_group_of_exactly_two_equal_digits,
    valid_passwords_in_range,
)


def aoc_2019_d4(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2019, 4, "Secure Container")
    io_handler.output_writer.write_header(problem_id)
    lower_bound, upper_bound = map(int, io_handler.input_reader.read().split("-"))
    criteria = [digits_are_increasing, two_adjacent_digits_are_the_same]
    valid_passwords = list(valid_passwords_in_range(lower_bound, upper_bound, criteria))
    yield ProblemSolution(
        problem_id,
        f"Number of valid passwords is {len(valid_passwords)}",
        part=1,
        result=len(valid_passwords),
    )

    criteria.append(at_least_one_group_of_exactly_two_equal_digits)
    valid_passwords = list(valid_passwords_in_range(lower_bound, upper_bound, criteria))
    yield ProblemSolution(
        problem_id,
        f"Number of valid passwords with the new criteria is {len(valid_passwords)}",
        part=2,
        result=len(valid_passwords),
    )
