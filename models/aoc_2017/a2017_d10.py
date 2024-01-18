from typing import Iterator


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

    def dense_hash(self) -> Iterator[int]:
        for i in range(0, len(self._list), 16):
            num = 0
            for j in range(16):
                num ^= self._list[i + j]
            yield num

    def _roll_left(self) -> None:
        self._list = (
            self._list[self._current_position :] + self._list[: self._current_position]
        )

    def _roll_right(self) -> None:
        self._list = (
            self._list[-self._current_position :]
            + self._list[: -self._current_position]
        )

    def _invert_sublist(self, length: int) -> None:
        self._list[:length] = self._list[:length][::-1]


def knot_hash(
    input: str,
    list_length: int = 256,
    num_rounds=64,
    suffix: tuple[int] = (17, 31, 73, 47, 23),
) -> list[int]:
    input_bytes = [ord(c) for c in input] + list(suffix)
    knot_hash = KnotHash(list_length)
    for _ in range(num_rounds):
        for length in input_bytes:
            knot_hash.iterate_hash(length)
    return list(knot_hash.dense_hash())
