import os
from models.common.io import IOHandler, ExecutionFlags
from models.aoc_2015 import ALL_2015_SOLUTIONS
from models.aoc_2016 import ALL_2016_SOLUTIONS
from models.aoc_2017 import ALL_2017_SOLUTIONS
from models.aoc_2018 import ALL_2018_SOLUTIONS
from models.aoc_2019 import ALL_2019_SOLUTIONS
from models.aoc_2020 import ALL_2020_SOLUTIONS
from models.aoc_2021 import ALL_2021_SOLUTIONS
from models.aoc_2022 import ALL_2022_SOLUTIONS
from .cli import InputFromTextFile, CliProgressBar, CliOutputWriter, JsonResultChecker


def _get_input_path(year: int, day: int) -> str:
    return os.path.join("files", "input_files", f"aoc_{year}", f"a{year}_d{day}.txt")


def _get_result_checker() -> JsonResultChecker:
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
    }
    result_checker = _get_result_checker()
    for year, days in problems.items():
        if len(days) == 0:
            days = [i + 1 for i in range(len(solutions[year]))]
        for day in days:
            file_name = _get_input_path(year, day)
            io_handler = IOHandler(
                input_reader=InputFromTextFile(file_name),
                output_writer=CliOutputWriter(flags),
                progress_bar=CliProgressBar(),
                execution_flags=flags,
                result_checker=result_checker,
            )
            solutions[year][day - 1](io_handler)
    if flags.check_results:
        _report_wrong_results(result_checker)


def _report_wrong_results(result_checker):
    print()
    wrong_results = list(result_checker.wrong_results())
    if not wrong_results:
        print("All results are correct!")
    else:
        print("The following results are incorrect:")
        for wrong_result in wrong_results:
            print(wrong_result)
