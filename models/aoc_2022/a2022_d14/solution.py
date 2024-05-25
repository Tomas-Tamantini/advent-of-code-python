from models.common.io import InputReader
from models.common.vectors import Vector2D
from .parser import parse_obstacles
from .falling_sand import FallingSand


def aoc_2022_d14(input_reader: InputReader, **_) -> None:
    print("--- AOC 2022 - Day 14: Regolith Reservoir ---")
    obstacles = set(parse_obstacles(input_reader))
    sand_pour_position = Vector2D(500, 0)
    falling_sand = FallingSand(sand_pour_position, obstacles)
    falling_sand.pour_until_steady_state()
    num_resting = len(falling_sand.resting_sand_positions)
    print(f"Part 1: Number of resting sand grains is {num_resting}")
