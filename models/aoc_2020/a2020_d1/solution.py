from models.common.io import IOHandler
from .subset_sum import subsets_that_sum_to


def aoc_2020_d1(io_handler: IOHandler, **_) -> None:
    print("--- AOC 2020 - Day 1: Report Repair ---")
    entries = [int(line) for line in io_handler.input_reader.readlines()]
    target_sum = 2020
    a, b = next(subsets_that_sum_to(target_sum, subset_size=2, entries=entries))
    print(f"Part 1: The two entries multiply to {a * b}")
    a, b, c = next(subsets_that_sum_to(target_sum, subset_size=3, entries=entries))
    print(f"Part 2: The three entries multiply to {a * b * c}")
