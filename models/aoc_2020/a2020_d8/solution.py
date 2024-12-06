from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .logic import find_and_run_game_console_which_terminates, run_game_console
from .parser import parse_game_console_instructions


def aoc_2020_d8(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2020, 8, "Handheld Halting")
    io_handler.output_writer.write_header(problem_id)
    instructions = list(parse_game_console_instructions(io_handler.input_reader))
    result = run_game_console(instructions)
    yield ProblemSolution(
        problem_id, f"The accumulator value is {result}", result, part=1
    )

    result = find_and_run_game_console_which_terminates(instructions)
    yield ProblemSolution(
        problem_id,
        f"The accumulator value in program which terminates is {result}",
        result,
        part=2,
    )
