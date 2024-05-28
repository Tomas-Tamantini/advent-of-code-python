from models.common.io import InputReader
from .air_conditioner import run_air_conditioner_program


def aoc_2019_d5(input_reader: InputReader, **_) -> None:
    print("--- AOC 2019 - Day 5: Sunny with a Chance of Asteroids ---")
    instructions = [int(code) for code in input_reader.read().split(",")]
    output_1 = run_air_conditioner_program(instructions, air_conditioner_id=1)
    print(f"Part 1: Diagnostic code for air conditioner 1 is {output_1}")
    output_5 = run_air_conditioner_program(instructions, air_conditioner_id=5)
    print(f"Part 2: Diagnostic code for air conditioner 5 is {output_5}")
