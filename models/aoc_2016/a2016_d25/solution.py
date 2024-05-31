from models.common.io import InputReader
from models.aoc_2016.assembunny import (
    parse_assembunny_code,
)
from .clock_signal import smallest_value_to_send_clock_signal


def aoc_2016_d25(input_reader: InputReader, **_) -> None:
    print("--- AOC 2016 - Day 25: Clock Signal ---")
    program = parse_assembunny_code(input_reader)
    smallest_value = smallest_value_to_send_clock_signal(program)
    print(f"Smallest value to send clock signal: {smallest_value}")
