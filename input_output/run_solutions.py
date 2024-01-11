from .a2015 import (
    aoc_2015_d1,
    aoc_2015_d2,
    aoc_2015_d3,
    aoc_2015_d4,
    aoc_2015_d5,
    aoc_2015_d6,
    aoc_2015_d7,
    aoc_2015_d8,
    aoc_2015_d9,
    aoc_2015_d10,
    aoc_2015_d11,
    aoc_2015_d12,
    aoc_2015_d13,
    aoc_2015_d14,
    aoc_2015_d15,
    aoc_2015_d16,
    aoc_2015_d17,
    aoc_2015_d18,
    aoc_2015_d19,
    aoc_2015_d20,
    aoc_2015_d21,
    aoc_2015_d22,
    aoc_2015_d23,
    aoc_2015_d24,
    aoc_2015_d25,
)
from .a2016 import aoc_2016_d1, aoc_2016_d2


def run_solutions(problems: dict[int, tuple[int, ...]]) -> None:
    solutions = {
        2015: (
            aoc_2015_d1,
            aoc_2015_d2,
            aoc_2015_d3,
            aoc_2015_d4,
            aoc_2015_d5,
            aoc_2015_d6,
            aoc_2015_d7,
            aoc_2015_d8,
            aoc_2015_d9,
            aoc_2015_d10,
            aoc_2015_d11,
            aoc_2015_d12,
            aoc_2015_d13,
            aoc_2015_d14,
            aoc_2015_d15,
            aoc_2015_d16,
            aoc_2015_d17,
            aoc_2015_d18,
            aoc_2015_d19,
            aoc_2015_d20,
            aoc_2015_d21,
            aoc_2015_d22,
            aoc_2015_d23,
            aoc_2015_d24,
            aoc_2015_d25,
        ),
        2016: (aoc_2016_d1, aoc_2016_d2),
    }
    for year, days in problems.items():
        if len(days) == 0:
            days = [i + 1 for i in range(len(solutions[year]))]
        for day in days:
            file_name = f"input_files/aoc_{year}/a{year}_d{day}.txt"
            solutions[year][day - 1](file_name)
