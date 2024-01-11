from models.vectors import Vector2D, CardinalDirection
from typing import Iterable


class Keypad:
    def __init__(self, initial_key: int) -> None:
        self._coords = self._key_to_coords(initial_key)

    def _key_to_coords(self, key: int) -> Vector2D:
        return Vector2D(
            x=(key - 1) % 3,
            y=2 - (key - 1) // 3,
        )

    def _coords_to_key(self, coords: Vector2D) -> int:
        return (2 - coords.y) * 3 + coords.x + 1

    @staticmethod
    def _is_out_of_bounds(coords: Vector2D) -> bool:
        return coords.x < 0 or coords.x > 2 or coords.y < 0 or coords.y > 2

    def move_to_adjacent_key(self, direction: CardinalDirection) -> None:
        new_coords = self._coords.move(direction)
        if self._is_out_of_bounds(new_coords):
            return
        self._coords = new_coords

    def move_multiple_keys(self, directions: Iterable[CardinalDirection]) -> None:
        for direction in directions:
            self.move_to_adjacent_key(direction)

    @property
    def key(self) -> int:
        return self._coords_to_key(self._coords)
