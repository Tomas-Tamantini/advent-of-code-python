from models.common.io import InputReader
from .rucksack import Rucksack


def aoc_2022_d3(input_reader: InputReader, **_) -> None:
    print("--- AOC 2022 - Day 3: Rucksack Reorganization ---")
    total_priorities = 0
    for items in input_reader.read_stripped_lines():
        rucksack = Rucksack(
            left_items=items[: len(items) // 2], right_items=items[len(items) // 2 :]
        )
        for common in rucksack.items_in_common():
            total_priorities += rucksack.item_priority(common)
    print(f"Part 1: Total priority of common items is {total_priorities}")
