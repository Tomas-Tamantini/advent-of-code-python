from models.common.io import IOHandler
from .bit_frequency import BitFrequency


def aoc_2021_d3(io_handler: IOHandler) -> None:
    print("--- AOC 2021 - Day 3: Binary Diagnostic ---")
    binary_strings = [line.strip() for line in io_handler.input_reader.readlines()]
    frequency = BitFrequency(binary_strings)
    most_frequent = frequency.most_frequent_bits_in_each_position()
    least_frequent = frequency.least_frequent_bits_in_each_position()
    product = int(most_frequent, 2) * int(least_frequent, 2)
    print(f"Part 1: The product of the most and least frequent bits is {product}")

    filtered_most_frequent = frequency.filter_down_to_one(filter_by_most_common=True)
    filtered_least_frequent = frequency.filter_down_to_one(filter_by_most_common=False)
    product = int(filtered_most_frequent, 2) * int(filtered_least_frequent, 2)
    print(
        f"Part 2: The product of the most and least frequent bits in filtered strings is {product}"
    )
