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

    @staticmethod
    def value_after_zero(offset: int, insertions: int) -> int:
        value_after_zero = -1
        insert_pos = 0
        for i in range(1, insertions + 1):
            insert_pos = (insert_pos + offset + 1) % i
            if insert_pos == 0:
                value_after_zero = i
        return value_after_zero
