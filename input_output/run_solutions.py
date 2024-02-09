from .a2015 import ALL_2015_SOLUTIONS
from .a2016 import ALL_2016_SOLUTIONS
from .a2017 import ALL_2017_SOLUTIONS
from .a2018 import ALL_2018_SOLUTIONS
from .a2019 import ALL_2019_SOLUTIONS


def run_solutions(problems: dict[int, tuple[int, ...]]) -> None:
    solutions = {
        2015: ALL_2015_SOLUTIONS,
        2016: ALL_2016_SOLUTIONS,
        2017: ALL_2017_SOLUTIONS,
        2018: ALL_2018_SOLUTIONS,
        2019: ALL_2019_SOLUTIONS,
    }
    for year, days in problems.items():
        if len(days) == 0:
            days = [i + 1 for i in range(len(solutions[year]))]
        for day in days:
            file_name = f"input_files/aoc_{year}/a{year}_d{day}.txt"
            solutions[year][day - 1](file_name)
