from models.common.io import InputReader
from .adapter_array import AdapterArray


def aoc_2020_d10(input_reader: InputReader, **_) -> None:
    print("--- AOC 2020 - Day 10: Adapter Array ---")
    adapters = [int(line) for line in input_reader.readlines()]
    array = AdapterArray(
        outlet_joltage=0,
        device_joltage=max(adapters) + 3,
        max_joltage_difference=3,
        adapter_ratings=adapters,
    )
    differences = array.joltage_differences_of_sorted_adapters()
    num_1_diff = differences.count(1)
    num_3_diff = differences.count(3)
    print(f"Part 1: {num_1_diff * num_3_diff} joltage differences")
    num_arrangements = array.number_of_arrangements()
    print(f"Part 2: {num_arrangements} arrangements")
