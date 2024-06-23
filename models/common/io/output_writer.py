from typing import Protocol, Optional
from dataclasses import dataclass


@dataclass(frozen=True)
class Problem:
    year: int
    day: int
    title: str


@dataclass(frozen=True)
class ProblemSolution:
    problem_id: Problem
    solution_text: str
    result: str = ""
    part: Optional[int] = None


class OutputWriter(Protocol):
    def write_header(self, problem: Problem) -> None: ...

    def write_solution(self, solution: ProblemSolution) -> None: ...

    def give_time_estimation(
        self, time_estimation: str, part: Optional[int] = None
    ) -> None: ...
