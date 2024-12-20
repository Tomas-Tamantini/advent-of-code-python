import importlib
import os
import re
from typing import Callable, Iterator

from models.common.io import ExecutionFlags, IOHandler, ProblemSolution, ResultChecker

from .cli import CliOutputWriter, CliProgressBar, InputFromTextFile, JsonResultChecker


def _get_input_path(year: int, day: int) -> str:
    return os.path.join("files", "input_files", f"aoc_{year}", f"a{year}_d{day}.txt")


def _get_result_checker() -> ResultChecker:
    expected_results_path = os.path.join("files", "expected_results.json")
    return JsonResultChecker(expected_results_path)


def _get_all_solutions(
    year: int,
) -> dict[int, Callable[[IOHandler], Iterator[ProblemSolution]]]:
    try:
        module = importlib.import_module(f"models.aoc_{year}")
        return getattr(module, f"ALL_{year}_SOLUTIONS")
    except (ModuleNotFoundError, AttributeError):
        raise ValueError(f"No solutions found for year {year}")


def available_years() -> Iterator[int]:
    for entry in os.scandir("models"):
        match = re.match(r"aoc_(\d{4})", entry.name)
        if match:
            yield int(match.group(1))


def run_solutions(problems: dict[int, tuple[int, ...]], flags: ExecutionFlags) -> None:
    result_checker = _get_result_checker()
    for year, days in problems.items():
        actual_days = days
        solutions = _get_all_solutions(year)
        if not actual_days:
            # TODO: Do this in main.py, not here
            actual_days = sorted(solutions.keys())
        for day in actual_days:
            file_name = _get_input_path(year, day)
            io_handler = IOHandler(
                input_reader=InputFromTextFile(file_name),
                output_writer=CliOutputWriter(flags),
                progress_bar=CliProgressBar(),
                execution_flags=flags,
                result_checker=result_checker,
            )
            for solution in solutions[day](io_handler):
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
