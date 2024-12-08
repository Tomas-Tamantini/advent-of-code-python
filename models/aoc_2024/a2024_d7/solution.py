from typing import Iterator, Optional

from models.common.io import IOHandler, Problem, ProblemSolution, ProgressBar

from .logic import Equation, is_valid_equation
from .parser import parse_equations


def _valid_equations(
    equations: list[Equation],
    possible_operators,
    progress_bar: Optional[ProgressBar] = None,
) -> Iterator[Equation]:
    for i, equation in enumerate(equations):
        if progress_bar:
            progress_bar.update(i, len(equations))
        if is_valid_equation(equation, possible_operators):
            yield equation


def aoc_2024_d7(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 7, "Bridge Repair")
    io_handler.output_writer.write_header(problem_id)
    equations = list(parse_equations(io_handler.input_reader))

    operators_part_1 = (
        lambda x, y: x + y,
        lambda x, y: x * y,
    )
    calibration_1 = sum(
        equation.test_value
        for equation in _valid_equations(equations, operators_part_1)
    )

    yield ProblemSolution(
        problem_id,
        f"The calibration result for valid equations with + and * is {calibration_1}",
        result=calibration_1,
        part=1,
    )

    operators_part_2 = operators_part_1 + (lambda x, y: int(f"{x}{y}"),)
    calibration_2 = sum(
        equation.test_value
        for equation in _valid_equations(
            equations, operators_part_2, io_handler.progress_bar
        )
    )
    yield ProblemSolution(
        problem_id,
        (
            "The calibration result for valid equations with +, *, "
            f"and concatenation is {calibration_2}"
        ),
        result=calibration_2,
        part=2,
    )
