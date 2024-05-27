from models.common.io import InputReader


def num_increases(lst: list[int]) -> int:
    return sum(lst[i] > lst[i - 1] for i in range(1, len(lst)))


def window_sum(lst: list[int], window_size: int) -> list[int]:
    return [sum(lst[i : i + window_size]) for i in range(len(lst) - window_size + 1)]


def aoc_2021_d1(input_reader: InputReader, **_) -> None:
    print("--- AOC 2021 - Day 1: Sonar Sweep ---")
    measurements = [int(line) for line in input_reader.readlines()]

    print(
        f"Part 1: The number of measurement increases is {num_increases(measurements)}"
    )
    sums = window_sum(measurements, window_size=3)
    print(f"Part 2: The number of increases in partial sums is {num_increases(sums)}")
