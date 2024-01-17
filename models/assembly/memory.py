from typing import Protocol


class Memory(Protocol):
    def get_at(self, index: int) -> int:
        ...

    def update_at(self, index: int, new_value) -> None:
        ...
