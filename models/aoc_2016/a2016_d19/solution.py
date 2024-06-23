from models.common.io import IOHandler
from .josephus import josephus, modified_josephus


def aoc_2016_d19(io_handler: IOHandler, **_) -> None:
    print("--- AOC 2016 - Day 19: An Elephant Named Joseph ---")
    num_elves = int(io_handler.input_reader.read().strip())
    winning_elf_take_left = josephus(num_elves)
    print(f"Part 1: Winning elf if they take from the left: {winning_elf_take_left}")
    winning_elf_take_across = modified_josephus(num_elves)
    print(f"Part 2: Winning elf if they take from across: {winning_elf_take_across}")
