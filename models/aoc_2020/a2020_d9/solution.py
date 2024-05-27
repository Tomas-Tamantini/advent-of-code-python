from models.common.io import InputReader
from .xmas_encoding import XMasEncoding


def aoc_2020_d9(input_reader: InputReader, **_) -> None:
    print("--- AOC 2020 - Day 9: Encoding Error ---")
    numbers = [int(line) for line in input_reader.readlines()]
    encoding = XMasEncoding(preamble_length=25)
    invalid_number = next(encoding.invalid_numbers(numbers))
    print(f"Part 1: The first invalid number is {invalid_number}")
    contiguous_numbers = next(
        encoding.contiguous_numbers_which_sum_to_target(numbers, target=invalid_number)
    )
    min_num, max_num = min(contiguous_numbers), max(contiguous_numbers)
    result = min_num + max_num
    print(f"Part 2: The sum of min and max contiguous numbers is {result}")
