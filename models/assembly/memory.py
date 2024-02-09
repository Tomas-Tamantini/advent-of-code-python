from typing import Protocol


class Memory(Protocol):
    def read(self, index: int) -> int:
        ...

    def write(self, index: int, new_value) -> None:
        ...
