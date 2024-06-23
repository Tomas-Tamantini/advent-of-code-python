from models.common.io import IOHandler
from .parser import parse_interval_pairs


def aoc_2022_d4(io_handler: IOHandler) -> None:
    print("--- AOC 2022 - Day 4: Camp Cleanup ---")
    pairs = list(parse_interval_pairs(io_handler.input_reader))
    num_pairs_fully_contained = sum(
        interval_a.is_contained_by(interval_b) or interval_b.is_contained_by(interval_a)
        for interval_a, interval_b in pairs
    )
    print(
        f"Part 1: Number of pairs in which one interval contains the other is {num_pairs_fully_contained}"
    )

    num_pairs_with_overlap = sum(
        interval_a.intersection(interval_b) is not None
        for interval_a, interval_b in pairs
    )
    print(f"Part 2: Number of pairs with some overlap {num_pairs_with_overlap}")
