from typing import Protocol


class OutputWriter(Protocol):
    def write_header(self, year: int, day: int, problem_title: str) -> None: ...
