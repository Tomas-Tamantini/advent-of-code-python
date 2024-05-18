from typing import Protocol


class ProgressBar(Protocol):
    def update(self, step: int, expected_num_steps: int) -> None: ...


class ProgressBarConsole:
    def __init__(self, message: str = "") -> None:
        self._last_percentage_point = -1
        self._message = message

    def set_message(self, message: str) -> None:
        self._message = message

    def update(self, step: int, expected_num_steps: int) -> None:
        current_percentage_point = (100 * step) // expected_num_steps
        if current_percentage_point != self._last_percentage_point:
            self._last_percentage_point = current_percentage_point
            print(f"{self._message} - {current_percentage_point}% complete", end="\r")
