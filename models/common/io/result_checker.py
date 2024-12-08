from dataclasses import dataclass
from typing import Iterator, Optional, Protocol

from .output_writer import Problem, ProblemSolution


@dataclass(frozen=True)
class WrongResult:
    problem_id: Problem
    expected: str
    received: str
    part: Optional[int] = None

    def __str__(self) -> str:
        header = (
            "Wrong result for problem "
            f"{self.problem_id.year} - day {self.problem_id.day}"
        )
        if self.part is not None:
            header += f" - Part {self.part}"
        return f"{header}\nExpected: {self.expected}\nReceived: {self.received}"


class ResultChecker(Protocol):
    def check_solution(self, solution: ProblemSolution) -> None: ...

    def wrong_results(self) -> Iterator[WrongResult]: ...

    @property
    def number_of_solutions(self) -> int: ...
