from models.common.io import IOHandler
from .parser import parse_crates


def aoc_2022_d5(io_handler: IOHandler) -> None:
    print("--- AOC 2022 - Day 5: Supply Stacks ---")
    parsed_crates = parse_crates(io_handler.input_reader, move_one_at_a_time=True)
    crates = parsed_crates.crates
    for move in parsed_crates.moves:
        move.apply(crates)
    top_items = "".join(crate.peek() for _, crate in sorted(crates.items()))
    print(f"Part 1: Items on top of crates when moving one at a time are {top_items}")

    parsed_crates = parse_crates(io_handler.input_reader, move_one_at_a_time=False)
    crates = parsed_crates.crates
    for move in parsed_crates.moves:
        move.apply(crates)
    top_items = "".join(crate.peek() for _, crate in sorted(crates.items()))
    print(f"Part 2: Items on top of crates when moving all at once are {top_items}")
