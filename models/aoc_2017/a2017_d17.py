class CircularBuffer:
    def __init__(self) -> None:
        self._values = [0]

    @property
    def values(self) -> list[int]:
        return self._values

    @property
    def value_at_current_position(self) -> int:
        return self._values[0]

    def insert_and_update_current_position(self, value: int, offset: int) -> None:
        insert_pos = (offset + 1) % len(self._values)
        self._values = [value] + self._values[insert_pos:] + self._values[:insert_pos]
