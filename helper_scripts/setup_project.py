import json
import os
from typing import Optional

from .fetch_problem_name import fetch_problem_name


def setup_project(
    year: int,
    day: int,
    problem_name: Optional[str] = None,
    parser_method_name: Optional[str] = None,
    create_empty_input_file: bool = True,
    create_expected_result_template: bool = True,
) -> None:
    if problem_name is None:
        problem_name = fetch_problem_name(year, day)
    solution_path = os.path.join("models", f"aoc_{year}", f"a{year}_d{day}")
    os.makedirs(solution_path, exist_ok=False)
    _create_solution_file(year, day, problem_name, solution_path, parser_method_name)
    _create_init_file(year, day, solution_path)
    if parser_method_name:
        test_path = os.path.join(solution_path, "tests")
        _create_test_folder(test_path)
        _create_parser_file(solution_path, parser_method_name)
        _create_parser_test_file(parser_method_name, test_path)
    if create_empty_input_file:
        _create_empty_input_file(year, day)
    if create_expected_result_template:
        _create_expected_result_template(year, day, problem_name)


def _create_solution_file(
    year: int,
    day: int,
    problem_name: str,
    solution_path: str,
    parser_method_name: Optional[str],
) -> None:
    with open(os.path.join(solution_path, "solution.py"), "w") as f:
        f.write("from typing import Iterator\n")
        f.write("from models.common.io import IOHandler, Problem, ProblemSolution\n")
        if parser_method_name:
            f.write(f"from .parser import {parser_method_name}\n")
        f.write(
            f"\n\ndef aoc_{year}_d{day}(io_handler: IOHandler) -> Iterator[ProblemSolution]:\n"
        )
        f.write(f'    problem_id = Problem({year}, {day}, "{problem_name}")\n')
        f.write("    io_handler.output_writer.write_header(problem_id)\n")
        f.write("    yield from []\n")


def _create_test_folder(test_path: str) -> None:
    os.makedirs(test_path, exist_ok=False)
    with open(os.path.join(test_path, "__init__.py"), "w") as _:
        ...


def _create_init_file(year: int, day: int, solution_path: str) -> None:
    with open(os.path.join(solution_path, "__init__.py"), "w") as f:
        f.write(f"from .solution import aoc_{year}_d{day}\n")


def _create_parser_file(solution_path: str, parser_method_name: str) -> None:
    with open(os.path.join(solution_path, "parser.py"), "w") as f:
        f.write("from models.common.io import InputReader\n")
        f.write("\n\n")
        f.write(
            f'def {parser_method_name}(input_reader: InputReader) -> "InsertReturnType":\n'
        )
        f.write("    pass\n")


def _create_parser_test_file(parser_method_name: str, test_path: str) -> None:
    with open(os.path.join(test_path, "test_parser.py"), "w") as f:
        f.write("from models.common.io import InputFromString\n")
        f.write(f"from ..parser import {parser_method_name}\n")
        f.write("\n\n")
        f.write(f"def test_{parser_method_name}():\n")
        f.write('    file_content = ""\n')
        f.write("    input_reader = InputFromString(file_content)\n")
        f.write("    # TODO: Implement test\n")


def _create_empty_input_file(year: int, day: int) -> None:
    with open(
        os.path.join("files", "input_files", f"aoc_{year}", f"a{year}_d{day}.txt"), "w"
    ) as f:
        f.write("")


def _yearly_results(year: int, results_by_year: list) -> dict:
    for year_results in results_by_year:
        if year_results["year"] == year:
            return year_results
    yearly_results = {"year": year, "results_by_day": []}
    results_by_year.append(yearly_results)
    return yearly_results


def _create_expected_result_template(year: int, day: int, problem_name: str) -> None:
    file_path = os.path.join("files", "expected_results.json")
    with open(file_path, "r") as f:
        expected_results = json.load(f)
    results_by_year: list[dict] = expected_results.get("results_by_year", [])
    yearly_results = _yearly_results(year, results_by_year)
    results_by_day: list[dict] = yearly_results.get("results_by_day", [])
    if any(day_results["day"] == day for day_results in results_by_day):
        raise ValueError("Expected results already exist")
    new_result = {"day": day, "title": problem_name, "results": []}
    results_by_day.append(new_result)

    with open(file_path, "w") as f:
        json.dump(expected_results, f, indent=4)
