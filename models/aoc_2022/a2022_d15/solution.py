from models.common.io import InputReader
from .parser import parse_proximity_sensors
from .logic import num_positions_which_cannot_contain_beacon


def aoc_2022_d15(input_reader: InputReader, **_) -> None:
    print("--- AOC 2022 - Day 15: Beacon Exclusion Zone ---")
    sensors = list(parse_proximity_sensors(input_reader))
    num_positions = num_positions_which_cannot_contain_beacon(
        row=2_000_000, sensors=sensors
    )
    print(
        f"Part 1: Number of positions which cannot contain a beacon is {num_positions}"
    )
