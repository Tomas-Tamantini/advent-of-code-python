import os

from models.aoc_2015 import ALL_2015_SOLUTIONS
from models.aoc_2016 import ALL_2016_SOLUTIONS
from models.aoc_2017 import ALL_2017_SOLUTIONS
from models.aoc_2018 import ALL_2018_SOLUTIONS
from models.aoc_2019 import ALL_2019_SOLUTIONS
from models.aoc_2020 import ALL_2020_SOLUTIONS
from models.aoc_2021 import ALL_2021_SOLUTIONS
from models.aoc_2022 import ALL_2022_SOLUTIONS
from models.aoc_2023 import ALL_2023_SOLUTIONS
from models.aoc_2024 import ALL_2024_SOLUTIONS
from models.common.io import ExecutionFlags, IOHandler, ResultChecker

from .cli import CliOutputWriter, CliProgressBar, InputFromTextFile, JsonResultChecker


def _get_input_path(year: int, day: int) -> str:
    return os.path.join("files", "input_files", f"aoc_{year}", f"a{year}_d{day}.txt")


def _get_result_checker() -> ResultChecker:
    expected_results_path = os.path.join("files", "expected_results.json")
    return JsonResultChecker(expected_results_path)


def run_solutions(problems: dict[int, tuple[int, ...]], flags: ExecutionFlags) -> None:
    solutions = {
        2015: ALL_2015_SOLUTIONS,
        2016: ALL_2016_SOLUTIONS,
        2017: ALL_2017_SOLUTIONS,
        2018: ALL_2018_SOLUTIONS,
        2019: ALL_2019_SOLUTIONS,
        2020: ALL_2020_SOLUTIONS,
        2021: ALL_2021_SOLUTIONS,
        2022: ALL_2022_SOLUTIONS,
        2023: ALL_2023_SOLUTIONS,
        2024: ALL_2024_SOLUTIONS,
    }
    result_checker = _get_result_checker()
    for year, days in problems.items():
        actual_days = days
        if not actual_days == 0:
            actual_days = [i + 1 for i in range(len(solutions[year]))]
        for day in actual_days:
            file_name = _get_input_path(year, day)
            io_handler = IOHandler(
                input_reader=InputFromTextFile(file_name),
                output_writer=CliOutputWriter(flags),
                progress_bar=CliProgressBar(),
                execution_flags=flags,
                result_checker=result_checker,
            )
            for solution in solutions[year][day - 1](io_handler):
                io_handler.set_solution(solution)
    if flags.check_results:
        _report_wrong_results(result_checker)


def _report_wrong_results(result_checker: ResultChecker) -> None:
    print()
    wrong_results = list(result_checker.wrong_results())
    num_wrong = len(wrong_results)
    num_solutions = result_checker.number_of_solutions
    if not wrong_results:
        print(f"All results are correct! ({num_solutions}/{num_solutions})")
    else:
        print(f"The following results are incorrect ({num_wrong}/{num_solutions}):")
        for wrong_result in wrong_results:
            print(wrong_result)
