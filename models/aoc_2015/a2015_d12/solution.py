from models.common.io import InputReader
from .json_parser import sum_all_numbers_in_json


def aoc_2015_d12(input_reader: InputReader, **_) -> None:
    print("--- AOC 2015 - Day 12: JSAbacusFramework.io ---")
    json_str = input_reader.read()
    json_sum = sum_all_numbers_in_json(json_str)
    print(f"Part 1: Sum of all numbers in JSON is {json_sum}")
    json_sum_minus_red = sum_all_numbers_in_json(json_str, property_to_ignore="red")
    print(
        f"Part 2: Sum of all numbers in JSON ignoring 'red' property is {json_sum_minus_red}"
    )
