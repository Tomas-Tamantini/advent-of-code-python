from models.common.io import InputReader
from .parser import parse_game_console_instructions
from .logic import run_game_console, find_and_run_game_console_which_terminates


def aoc_2020_d8(input_reader: InputReader, **_) -> None:
    print("--- AOC 2020 - Day 8: Handheld Halting ---")
    instructions = list(parse_game_console_instructions(input_reader))
    accumulator = run_game_console(instructions)
    print(f"Part 1: The accumulator value is {accumulator}")
    accumulator = find_and_run_game_console_which_terminates(instructions)
    print(f"Part 2: The accumulator value in program which terminates is {accumulator}")
