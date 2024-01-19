class ProgressBarConsole:
    def __init__(self) -> None:
        self._last_percentage_point = -1

    def update(self, step: int, expected_num_steps: int) -> None:
        current_percentage_point = (100 * step) // expected_num_steps
        if current_percentage_point != self._last_percentage_point:
            self._last_percentage_point = current_percentage_point
            print(f" - {current_percentage_point}% complete", end="\r")
