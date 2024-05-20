from models.common.io import InputReader
from .parser import parse_interval_pairs


def aoc_2022_d4(input_reader: InputReader, **_) -> None:
    print("--- AOC 2022 - Day 4: Camp Cleanup ---")
    num_pairs_fully_contained = 0
    for interval_a, interval_b in parse_interval_pairs(input_reader):
        if interval_a.is_contained_by(interval_b) or interval_b.is_contained_by(
            interval_a
        ):
            num_pairs_fully_contained += 1
    print(
        f"Part 1: Number of pairs in which one interval contains the other is {num_pairs_fully_contained}"
    )
