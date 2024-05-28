from models.common.io import InputReader
from .square_spiral import SquareSpiral


def aoc_2017_d3(input_reader: InputReader, **_) -> None:
    print("--- AOC 2017 - Day 3: Spiral Memory ---")
    target = int(input_reader.read().strip())
    target_coordinates = SquareSpiral.coordinates(target)
    manhattan_distance = target_coordinates.manhattan_size
    print(f"Part 1: Manhattan distance to {target}: {manhattan_distance}")
    first_value_larger_than_input = -1
    for value in SquareSpiral.adjacent_sum_sequence():
        if value > target:
            first_value_larger_than_input = value
            break
    print(
        f"Part 2: First sequence term larger than {target}: {first_value_larger_than_input}"
    )
