from typing import Iterator
from models.common.io import IOHandler


def digits_that_match_the_next(sequence: str, wrap_around: bool) -> Iterator[chr]:
    for i in range(len(sequence) - 1):
        if sequence[i] == sequence[i + 1]:
            yield sequence[i]

    if wrap_around and sequence[0] == sequence[-1]:
        yield sequence[-1]


def digits_that_match_one_across_the_circle(sequence: str) -> Iterator[chr]:
    for i in range(len(sequence)):
        next_i = (i + len(sequence) // 2) % len(sequence)
        if sequence[i] == sequence[next_i]:
            yield sequence[i]


def aoc_2017_d1(io_handler: IOHandler) -> None:
    print("--- AOC 2017 - Day 1: Inverse Captcha ---")
    digit_sequence = io_handler.input_reader.read().strip()
    sum_matches = sum(
        int(d) for d in digits_that_match_the_next(digit_sequence, wrap_around=True)
    )
    print(f"Part 1: Sum of digits that match the next one: {sum_matches}")
    sum_matches = sum(
        int(d) for d in digits_that_match_one_across_the_circle(digit_sequence)
    )
    print(f"Part 2: Sum of digits that match one across the circle: {sum_matches}")
