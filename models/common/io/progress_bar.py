from typing import Protocol


class ProgressBar(Protocol):
    def update(self, step: int, expected_num_steps: int) -> None: ...
