from models.common.io import IOHandler
from models.aoc_2019.a2019_d5.air_conditioner import run_air_conditioner_program


def aoc_2019_d9(io_handler: IOHandler, **_) -> None:
    print("--- AOC 2019 - Day 9: Sensor Boost ---")
    instructions = [int(code) for code in io_handler.input_reader.read().split(",")]
    output = run_air_conditioner_program(instructions, air_conditioner_id=1)
    print(f"Part 1: Output for the BOOST program is {output}")
    output = run_air_conditioner_program(instructions, air_conditioner_id=2)
    print(f"Part 2: Coordinates of the distress signal are {output}")
