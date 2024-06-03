from models.common.io import InputReader
from .parser import parse_shuffled_seven_digit_displays


def aoc_2021_d8(input_reader: InputReader, **_) -> None:
    print("--- AOC 2021 - Day 8: Seven Segment Search ---")
    displays = list(parse_shuffled_seven_digit_displays(input_reader))
    decoded_digits = [display.decode() for display in displays]
    num_matches = sum(
        1 for digits in decoded_digits for digit in digits if digit in "1478"
    )
    print(f"Part 1: The number of 1, 4, 7, 8 in the decoded digits is {num_matches}")
    total_sum = sum(int(digits) for digits in decoded_digits)
    print(f"Part 2: The total sum of all decoded digits is {total_sum}")
