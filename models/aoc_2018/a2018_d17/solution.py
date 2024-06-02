from models.common.io import InputReader
from models.common.vectors import Vector2D
from .parser import parse_position_ranges
from .water_spring import WaterSpring


def aoc_2018_d17(input_reader: InputReader, **_) -> None:
    print("--- AOC 2018 - Day 17: Reservoir Research ---")
    clay_positions = set(parse_position_ranges(input_reader))
    spring_position = Vector2D(500, 0)
    water_spring = WaterSpring(spring_position, clay_positions)
    water_spring.flow()
    print(f"Part 1: Number of tiles with water: {water_spring.num_wet_tiles}")
    print(
        f"Part 2: Number of tiles with retained water: {water_spring.num_still_water_tiles}"
    )
