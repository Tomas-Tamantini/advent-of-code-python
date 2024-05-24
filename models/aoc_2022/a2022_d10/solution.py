from models.common.io import InputReader
from .parser import parse_instructions_with_duration
from .register_history import RegisterHistory


def aoc_2022_d10(input_reader: InputReader, **_) -> None:
    print("--- AOC 2022 - Day 10: Cathode-Ray Tube ---")
    rh = RegisterHistory()
    for instruction in parse_instructions_with_duration(input_reader):
        rh.run_instruction(instruction)
    strengths = [cycle * rh.value_during_cycle(cycle) for cycle in range(20, 221, 40)]
    print(
        f"Part 1: Sum of strengths at cycles 20, 60, 100, 140, and 180: {sum(strengths)}"
    )
