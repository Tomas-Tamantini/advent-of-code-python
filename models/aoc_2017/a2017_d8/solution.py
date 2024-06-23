from models.common.io import IOHandler
from .parser import parse_conditional_increment_instructions
from .conditional_increment import maximum_value_at_registers


def aoc_2017_d8(io_handler: IOHandler) -> None:
    print("--- AOC 2017 - Day 8: I Heard You Like Registers ---")
    instructions = list(
        parse_conditional_increment_instructions(io_handler.input_reader)
    )
    max_values = list(maximum_value_at_registers(instructions))
    max_value_final = max_values[-1]
    max_value_all_time = max(max_values)
    print(f"Part 1: Maximum register value at end: {max_value_final}")
    print(f"Part 2: Maximum register value at any time: {max_value_all_time}")
