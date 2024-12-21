from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .logic import (
    DIRECTIONAL_ROBOT,
    NUMERIC_ROBOT,
    KeypadRobots,
    min_num_keypad_presses,
)


def _numeric_part(code: str) -> int:
    return int(code[:-1])


def _complexity(code: str, num_directional_robots: int) -> int:
    min_presses = min_num_keypad_presses(
        code, NUMERIC_ROBOT, KeypadRobots(DIRECTIONAL_ROBOT, num_directional_robots)
    )
    return min_presses * _numeric_part(code)


def aoc_2024_d21(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 21, "Keypad Conundrum")
    io_handler.output_writer.write_header(problem_id)
    codes = [line for line in io_handler.input_reader.read_stripped_lines()]

    complexities_2 = sum(_complexity(code, 2) for code in codes)
    yield ProblemSolution(
        problem_id,
        f"The sum of complexities with 2 directional robots is {complexities_2}",
        result=complexities_2,
        part=1,
    )

    complexities_25 = sum(_complexity(code, 25) for code in codes)
    yield ProblemSolution(
        problem_id,
        f"The sum of complexities with 25 directional robots is {complexities_25}",
        result=complexities_25,
        part=2,
    )
