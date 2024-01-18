class KnotHash:
    def __init__(self, list_length: int) -> None:
        self._list = list(range(list_length))
        self._current_position = 0
        self._skip_size = 0

    @property
    def list(self) -> list[int]:
        return self._list

    def iterate_hash(self, length: int) -> None:
        if length > 1:
            self._roll_left()
            self._invert_sublist(length)
            self._roll_right()
        self._current_position = (
            self._current_position + length + self._skip_size
        ) % len(self._list)
        self._skip_size += 1

    def _roll_left(self):
        self._list = (
            self._list[self._current_position :] + self._list[: self._current_position]
        )

    def _roll_right(self):
        self._list = (
            self._list[-self._current_position :]
            + self._list[: -self._current_position]
        )

    def _invert_sublist(self, length):
        self._list = self._list[length - 1 :: -1] + self._list[length:]
