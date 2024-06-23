from typing import Protocol, Iterator, Optional
from dataclasses import dataclass
from .output_writer import ProblemSolution, Problem


@dataclass(frozen=True)
class WrongResult:
    problem_id: Problem
    expected: str
    received: str
    part: Optional[int] = None

    def __str__(self) -> str:
        header = f"Wrong result for problem {self.problem_id.year} - day {self.problem_id.day}"
        if self.part is not None:
            header += f" - Part {self.part}"
        return f"{header}\nExpected: {self.expected}\nReceived: {self.received}"


class ResultChecker(Protocol):
    def check_solution(self, solution: ProblemSolution) -> None: ...

    def wrong_results(self) -> Iterator[WrongResult]: ...
