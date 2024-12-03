from typing import Protocol


class ProgramStack(Protocol):
    @property
    def result(self) -> int: ...

    def increment_result(self, value: int) -> None: ...

    def enable_increment(self) -> None: ...

    def disable_increment(self) -> None: ...


class StackWithoutConditional:
    def __init__(self) -> None:
        self._result = 0

    @property
    def result(self) -> int:
        return self._result

    def increment_result(self, value: int) -> None:
        self._result += value

    def enable_increment(self) -> None:
        pass

    def disable_increment(self) -> None:
        pass


class StackWithConditional:
    def __init__(self) -> None:
        self._result = 0
        self._enabled = True

    @property
    def result(self) -> int:
        return self._result

    def increment_result(self, value: int) -> None:
        if self._enabled:
            self._result += value

    def enable_increment(self) -> None:
        self._enabled = True

    def disable_increment(self) -> None:
        self._enabled = False
