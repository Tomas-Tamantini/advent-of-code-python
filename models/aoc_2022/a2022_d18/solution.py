from models.common.io import InputReader
from .parser import parse_cube_positions
from .logic import total_surface_area


def aoc_2022_d18(input_reader: InputReader, **_) -> None:
    print("--- AOC 2022 - Day 18: Boiling Boulders ---")
    cubes = set(parse_cube_positions(input_reader))
    surface_area = total_surface_area(cubes)
    print(f"Part 1: Surface area of droplet is {surface_area}")
