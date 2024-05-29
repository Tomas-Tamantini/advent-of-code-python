from models.common.io import InputReader
from .valid_passwords import (
    digits_are_increasing,
    two_adjacent_digits_are_the_same,
    at_least_one_group_of_exactly_two_equal_digits,
    valid_passwords_in_range,
)


def aoc_2019_d4(input_reader: InputReader, **_) -> None:
    print("--- AOC 2019 - Day 4: Secure Container ---")
    lower_bound, upper_bound = map(int, input_reader.read().split("-"))
    criteria = [digits_are_increasing, two_adjacent_digits_are_the_same]
    valid_passwords = list(valid_passwords_in_range(lower_bound, upper_bound, criteria))
    print(f"Part 1: Number of valid passwords is {len(valid_passwords)}")
    criteria.append(at_least_one_group_of_exactly_two_equal_digits)
    valid_passwords = list(valid_passwords_in_range(lower_bound, upper_bound, criteria))
    print(
        f"Part 2: Number of valid passwords with the new criteria is {len(valid_passwords)}"
    )