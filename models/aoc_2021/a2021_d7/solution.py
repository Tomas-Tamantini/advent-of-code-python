from models.common.io import InputReader
from .optimal_fuel_consumption import (
    optimal_linear_fuel_consumption,
    optimal_triangular_fuel_consumption,
)


def aoc_2021_d7(input_reader: InputReader, **_) -> None:
    print("--- AOC 2021 - Day 7: The Treachery of Whales ---")
    positions = list(map(int, input_reader.read().split(",")))

    optimal_linear = optimal_linear_fuel_consumption(positions)
    print(
        f"Part 1: The total fuel required with linear consumption is {optimal_linear}"
    )

    optimal_triangular = optimal_triangular_fuel_consumption(positions)
    print(
        f"Part 2: The total fuel required with triangular consumption is {optimal_triangular}"
    )
