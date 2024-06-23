from models.common.io import IOHandler
from .parser import parse_string_scrambler


def aoc_2016_d21(io_handler: IOHandler) -> None:
    print("--- AOC 2016 - Day 21: Scrambled Letters and Hash ---")
    scrambler = parse_string_scrambler(io_handler.input_reader)
    password = scrambler.scramble("abcdefgh")
    print(f"Part 1: Password after scrambling: {password}")
    password = scrambler.unscramble("fbgdceah")
    print(f"Part 2: Password before scrambling: {password}")
