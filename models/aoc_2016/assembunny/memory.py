from typing import Protocol


class Memory(Protocol):
    def get(self, index: int) -> int:
        pass

    def update(self, index: int, new_value) -> None:
        pass
