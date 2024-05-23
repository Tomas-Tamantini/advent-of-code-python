from models.common.io import InputReader
from .parser import parse_file_tree


def aoc_2022_d7(input_reader: InputReader, **_) -> None:
    print("--- AOC 2022 - Day 7: No Space Left On Device ---")
    tree = parse_file_tree(input_reader)
    sum_small_directories = 0
    for dir in tree.all_directories():
        size = dir.size()
        if size <= 100_000:
            sum_small_directories += size
    print(f"Part 1: Sum of sizes of small directories is {sum_small_directories}")
