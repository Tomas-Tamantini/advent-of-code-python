from models.common.io import InputFromTextFile, ProgressBarConsole
from models.aoc_2015 import ALL_2015_SOLUTIONS
from models.aoc_2016 import ALL_2016_SOLUTIONS
from models.aoc_2017 import ALL_2017_SOLUTIONS
from models.aoc_2018 import ALL_2018_SOLUTIONS
from models.aoc_2019 import ALL_2019_SOLUTIONS
from models.aoc_2020 import ALL_2020_SOLUTIONS
from models.aoc_2021 import ALL_2021_SOLUTIONS
from models.aoc_2022 import ALL_2022_SOLUTIONS


def run_solutions(
    problems: dict[int, tuple[int, ...]], animate: bool, play: bool
) -> None:
    solutions = {
        2015: ALL_2015_SOLUTIONS,
        2016: ALL_2016_SOLUTIONS,
        2017: ALL_2017_SOLUTIONS,
        2018: ALL_2018_SOLUTIONS,
        2019: ALL_2019_SOLUTIONS,
        2020: ALL_2020_SOLUTIONS,
        2021: ALL_2021_SOLUTIONS,
        2022: ALL_2022_SOLUTIONS,
    }
    for year, days in problems.items():
        if len(days) == 0:
            days = [i + 1 for i in range(len(solutions[year]))]
        for day in days:
            file_name = f"input_files/aoc_{year}/a{year}_d{day}.txt"
            solutions[year][day - 1](
                input_reader=InputFromTextFile(file_name),
                progress_bar=ProgressBarConsole(),
                animate=animate,
                play=play,
            )
