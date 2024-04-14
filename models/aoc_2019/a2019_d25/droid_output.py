from typing import Protocol


class OutputHandler(Protocol):
    def handle_new_output_line(self, output_line: str) -> None: ...


class DroidOutput:
    def __init__(self, output_handler: OutputHandler) -> None:
        self._current_line = ""
        self._output_handler = output_handler

    def write(self, value: int) -> None:
        if value == ord("\n"):
            self._output_handler.handle_new_output_line(self._current_line)
            self._current_line = ""
        else:
            self._current_line += chr(value)
