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
    result: str
    part: Optional[int] = None
    supports_animation: bool = False
    supports_play: bool = False


class OutputWriter(Protocol):
    def write_header(self, problem: Problem) -> None: ...

    def write_solution(self, solution: ProblemSolution) -> None: ...

    def log_progress(self, progress_message: str) -> None: ...

    def log_error(self, error_message: str) -> None: ...

    def give_time_estimation(
        self, time_estimation: str, part: Optional[int] = None
    ) -> None: ...
