from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .logic import is_valid_equation
from .parser import parse_equations


def aoc_2024_d7(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 7, "Bridge Repair")
    io_handler.output_writer.write_header(problem_id)
    equations = list(parse_equations(io_handler.input_reader))

    possible_operators = (
        lambda x, y: x + y,
        lambda x, y: x * y,
    )
    total_valid_equations = 0
    for equation in equations:
        if is_valid_equation(equation, possible_operators):
            total_valid_equations += equation.test_value

    yield ProblemSolution(
        problem_id,
        f"The calibration result for valid equations is {total_valid_equations}",
        result=total_valid_equations,
        part=1,
    )
