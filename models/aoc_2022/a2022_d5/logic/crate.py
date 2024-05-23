from typing import Optional


class Crate:
    def __init__(self) -> None:
        self._items = []

    def push(self, item: chr) -> None:
        self._items.append(item)

    def pop(self) -> Optional[chr]:
        return self._items.pop()

    def peek(self) -> Optional[chr]:
        return self._items[-1] if self._items else None
