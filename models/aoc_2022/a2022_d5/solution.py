from models.common.io import InputReader
from .parser import parse_crates


def aoc_2022_d5(input_reader: InputReader, **_) -> None:
    print("--- AOC 2022 - Day 5: Supply Stacks ---")
    parsed_crates = parse_crates(input_reader)
    crates = parsed_crates.crates
    for move in parsed_crates.moves:
        move.apply(crates)
    top_items = ""
    for _, crate in sorted(crates.items()):
        top_items += crate.peek()
    print(f"Part 1: Items on top of crates are {top_items}")
