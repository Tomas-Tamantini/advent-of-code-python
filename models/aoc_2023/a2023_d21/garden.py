from abc import ABC, abstractmethod
from typing import Iterator
from models.common.vectors import Vector2D


class _Garden(ABC):
    def __init__(self, width: int, height: int, rock_positions: set[Vector2D]) -> None:
        self._width = width
        self._height = height
        self._rock_positions = rock_positions

    @abstractmethod
    def _is_valid_position(self, pos: Vector2D) -> bool: ...

    def neighboring_positions(self, position: Vector2D) -> Iterator[Vector2D]:
        for neighbor in position.adjacent_positions():
            if self._is_valid_position(neighbor):
                yield neighbor

    def next_positions(self, current_positions: set[Vector2D]) -> Iterator[Vector2D]:
        for pos in current_positions:
            yield from self.neighboring_positions(pos)


class BoundedGarden(_Garden):
    def _is_within_bounds(self, position: Vector2D) -> bool:
        return (0 <= position.x < self._width) and (0 <= position.y < self._height)

    def _is_valid_position(self, pos: Vector2D) -> bool:
        return self._is_within_bounds(pos) and pos not in self._rock_positions


class PacmanGarden(_Garden):
    def _is_valid_position(self, pos: Vector2D) -> bool:
        equivalent_pos = Vector2D(pos.x % self._width, pos.y % self._height)
        return equivalent_pos not in self._rock_positions
