from models.common.input_reader import InputReader
from .parser import parse_calories


def aoc_2022_d1(input_reader: InputReader, **_) -> None:
    print("--- AOC 2022 - Day 1: Calorie Counting ---")
    calories_by_elf = [sum(calories) for calories in parse_calories(input_reader)]
    sorted_calories = sorted(calories_by_elf)
    max_calories = sorted_calories[-1]
    print(f"Part 1: Maximum calories is {max_calories}")
    top_3_calories = sum(sorted_calories[-3:])
    print(f"Part 2: Sum of top 3 calories is {top_3_calories}")
