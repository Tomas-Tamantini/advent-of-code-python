from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .logic import CODE_ROBOT, DIRECTIONAL_ROBOT, min_num_keypad_presses


def _numeric_part(code: str) -> int:
    return int(code[:-1])


def aoc_2024_d21(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 21, "Keypad Conundrum")
    io_handler.output_writer.write_header(problem_id)
    codes = [line for line in io_handler.input_reader.read_stripped_lines()]

    complexities = 0
    for code in codes:
        min_presses = min_num_keypad_presses(
            code,
            code_robot=CODE_ROBOT,
            directional_robot=DIRECTIONAL_ROBOT,
            num_directional_robots=2,
        )
        complexities += min_presses * _numeric_part(code)

    yield ProblemSolution(
        problem_id,
        f"The sum of complexities is {complexities}",
        result=complexities,
        part=1,
    )
