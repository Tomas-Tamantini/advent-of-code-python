import json
from typing import Iterator
from models.common.io import ProblemSolution, WrongResult
from dataclasses import dataclass


@dataclass(frozen=True)
class _ResultKey:
    year: int
    day: int


class JsonResultChecker:
    def __init__(self, expected_results_path: str) -> None:
        self._path = expected_results_path
        self._wrong_results = []
        self._expected_results = dict()
        self._loaded_results = False
        self._checked_solutions = set()

    @property
    def number_of_solutions(self) -> int:
        return len(self._checked_solutions)

    def _load_expected_results(self) -> None:
        with open(self._path, "r") as file:
            data = json.load(file)
            results_by_year = data.get("results_by_year", [])
            for result_by_year in results_by_year:
                year = int(result_by_year.get("year", 0))
                results_by_day = result_by_year.get("results_by_day", [])
                for result_by_day in results_by_day:
                    day = int(result_by_day.get("day", 0))
                    results = result_by_day.get("results", [])
                    key = _ResultKey(year, day)
                    self._expected_results[key] = results
        self._loaded_results = True

    @staticmethod
    def _expected_not_found(solution: ProblemSolution) -> WrongResult:
        return WrongResult(
            solution.problem_id,
            expected="No expected result found",
            received=solution.result,
            part=solution.part,
        )

    def check_solution(self, solution: ProblemSolution) -> None:
        if not self._loaded_results:
            self._load_expected_results()
        self._checked_solutions.add(solution)
        key = _ResultKey(solution.problem_id.year, solution.problem_id.day)
        results = self._expected_results.get(key)
        part = solution.part or 1
        if not results or len(results) < part:
            self._wrong_results.append(self._expected_not_found(solution))
        else:
            expected = str(results[part - 1])
            if expected != str(solution.result):
                self._wrong_results.append(
                    WrongResult(
                        solution.problem_id,
                        expected=expected,
                        received=solution.result,
                        part=solution.part,
                    )
                )

    def wrong_results(self) -> Iterator[WrongResult]:
        yield from self._wrong_results
