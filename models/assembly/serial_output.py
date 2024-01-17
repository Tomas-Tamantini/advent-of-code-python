from typing import Protocol


class SerialOutput(Protocol):
    def write(self, value: int) -> None:
        ...
