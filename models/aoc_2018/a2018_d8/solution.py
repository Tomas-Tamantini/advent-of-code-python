from models.common.io import InputReader
from .navigation_tree import parse_list_into_navigation_tree


def aoc_2018_d8(input_reader: InputReader, **_) -> None:
    print("--- AOC 2018 - Day 8: Memory Maneuver ---")
    numbers = list(map(int, input_reader.read().split()))
    root = parse_list_into_navigation_tree(numbers)
    print(f"Part 1: Sum of metadata: {root.sum_of_metadata()}")
    print(f"Part 2: Value of root node: {root.navigation_value()}")
