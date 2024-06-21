from models.common.io import InputReader
from .parser import parse_blizzard_valley
from .logic import BlizzardMazeSolver


def aoc_2022_d24(input_reader: InputReader, **_) -> None:
    print("--- AOC 2022 - Day 24: Blizzard Basin ---")
    valley = parse_blizzard_valley(input_reader)
    solver = BlizzardMazeSolver(valley)
    min_steps = solver.min_steps_to_exit()
    print(f"Part 1: The minimum number of steps to exit valley is {min_steps}")
