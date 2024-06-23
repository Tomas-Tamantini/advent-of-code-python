from typing import Protocol, Optional
from dataclasses import dataclass


@dataclass(frozen=True)
class Problem:
    year: int
    day: int
    title: str


class OutputWriter(Protocol):
    def write_header(self, problem: Problem) -> None: ...

    def give_time_estimation(
        self, time_estimation: str, part: Optional[int] = None
    ) -> None: ...
