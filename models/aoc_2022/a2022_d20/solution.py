from models.common.io import InputReader
from .circular_encryption import mix_list


def aoc_2022_d20(input_reader: InputReader, **_) -> None:
    print("--- AOC 2022 - Day 20: Grove Positioning System ---")
    numbers = [int(line) for line in input_reader.read_stripped_lines()]
    shuffled_numbers = mix_list(numbers)
    zero_index = shuffled_numbers.index(0)
    indices = [(zero_index + i) % len(shuffled_numbers) for i in (1000, 2000, 3000)]
    total_sum = sum(shuffled_numbers[i] for i in indices)
    print(f"Part 1: Sum of numbers at positions 1000, 2000, and 3000: {total_sum}")
