from typing import Iterable

from models.common.vectors import CardinalDirection, Vector2D


class Keypad:
    def __init__(self, configuration: str, initial_key: chr) -> None:
        self._key_matrix: list[list[chr]] = [
            list(line.strip()) for line in configuration.splitlines()
        ]
        self._width = len(self._key_matrix[0])
        self._height = len(self._key_matrix)
        self._coords = self._key_to_coords(initial_key)

    def _key_to_coords(self, key: chr) -> Vector2D:
        for y, line in enumerate(self._key_matrix):
            for x, value in enumerate(line):
                if value == key:
                    return Vector2D(x, self._height - y - 1)

    def _coords_to_key(self, coords: Vector2D) -> chr:
        return self._key_matrix[self._height - coords.y - 1][coords.x]

    def _is_within_bounds(self, coords: Vector2D) -> bool:
        if (
            coords.x < 0
            or coords.y < 0
            or coords.x >= self._width
            or coords.y >= self._height
        ):
            return False
        return self._coords_to_key(coords) != "*"

    def move_to_adjacent_key(self, direction: CardinalDirection) -> None:
        new_coords = self._coords.move(direction)
        if self._is_within_bounds(new_coords):
            self._coords = new_coords

    def move_multiple_keys(self, directions: Iterable[CardinalDirection]) -> None:
        for direction in directions:
            self.move_to_adjacent_key(direction)

    @property
    def key(self) -> chr:
        return self._coords_to_key(self._coords)
