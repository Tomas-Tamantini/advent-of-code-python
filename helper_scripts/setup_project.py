import os
from typing import Optional
from .fetch_problem_name import fetch_problem_name


def setup_project(year: int, day: int, problem_name: Optional[str] = None) -> None:
    if problem_name is None:
        problem_name = fetch_problem_name(year, day)
    solution_path = os.path.join("models", f"aoc_{year}", f"a{year}_d{day}")
    os.makedirs(solution_path, exist_ok=False)
    _create_solution_file(year, day, problem_name, solution_path)
    _create_init_file(year, day, solution_path)


def _create_solution_file(year, day, problem_name, solution_path):
    with open(os.path.join(solution_path, "solution.py"), "w") as f:
        f.write("from models.common.io import InputReader\n\n\n")
        f.write(f"def aoc_{year}_d{day}(input_reader: InputReader, **_) -> None:\n")
        f.write(f'    print("--- AOC {year} - Day {day}: {problem_name} ---")\n')


def _create_init_file(year, day, solution_path):
    with open(os.path.join(solution_path, "__init__.py"), "w") as f:
        f.write(f"from .solution import aoc_{year}_d{day}\n")
