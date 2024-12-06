from queue import Queue
from typing import Any


class DroidInput:
    def __init__(self) -> None:
        self._command_queue = Queue()
        self._current_command_iterator = None

    def give_command(self, command: Any) -> None:
        self._command_queue.put(command)

    def _next_character(self) -> chr:
        if self._current_command_iterator is None:
            if self._command_queue.empty():
                raise ValueError("No command has been given")
            self._current_command_iterator = iter(str(self._command_queue.get()))
        try:
            return next(self._current_command_iterator)
        except StopIteration:
            self._current_command_iterator = None
            return "\n"

    def read(self) -> int:
        return ord(self._next_character())
