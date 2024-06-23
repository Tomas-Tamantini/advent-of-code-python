from models.common.io import IOHandler, Problem
from .parser import parse_game_console_instructions
from .logic import run_game_console, find_and_run_game_console_which_terminates


def aoc_2020_d8(io_handler: IOHandler) -> None:
    problem_id = Problem(2020, 8, "Handheld Halting")
    io_handler.output_writer.write_header(problem_id)
    instructions = list(parse_game_console_instructions(io_handler.input_reader))
    accumulator = run_game_console(instructions)
    print(f"Part 1: The accumulator value is {accumulator}")
    accumulator = find_and_run_game_console_which_terminates(instructions)
    print(f"Part 2: The accumulator value in program which terminates is {accumulator}")
