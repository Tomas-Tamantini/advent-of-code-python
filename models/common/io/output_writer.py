from typing import Protocol, Optional


class OutputWriter(Protocol):
    def write_header(self, year: int, day: int, problem_title: str) -> None: ...

    def give_time_estimation(
        self, time_estimation: str, part: Optional[int] = None
    ) -> None: ...
