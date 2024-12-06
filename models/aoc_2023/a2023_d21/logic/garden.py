from dataclasses import dataclass
from typing import Protocol

from models.common.vectors import Vector2D


class Garden(Protocol):
    def is_valid_position(self, position: Vector2D) -> bool: ...


@dataclass(frozen=True)
class BoundedGarden:
    width: int
    height: int
    rock_positions: set[Vector2D]

    def _is_within_bounds(self, position: Vector2D) -> bool:
        return (0 <= position.x < self.width) and (0 <= position.y < self.height)

    def is_valid_position(self, position: Vector2D) -> bool:
        return self._is_within_bounds(position) and position not in self.rock_positions


@dataclass(frozen=True)
class InfiniteGarden:
    width: int
    height: int
    rock_positions: set[Vector2D]

    def is_valid_position(self, position: Vector2D) -> bool:
        equivalent_pos = Vector2D(position.x % self.width, position.y % self.height)
        return equivalent_pos not in self.rock_positions
