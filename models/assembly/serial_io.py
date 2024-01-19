from typing import Protocol


class SerialInput(Protocol):
    def read(self) -> int:
        ...


class SerialOutput(Protocol):
    def write(self, value: int) -> None:
        ...
