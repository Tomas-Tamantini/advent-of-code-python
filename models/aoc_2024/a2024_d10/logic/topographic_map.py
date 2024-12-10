from typing import Iterator

from models.common.io import CharacterGrid
from models.common.vectors import Vector2D

from .trail import HikingTrail


class TopographicMap:
    def __init__(self, grid: CharacterGrid):
        self._grid = grid

    def _is_destination(self, position: Vector2D) -> bool:
        return self._grid.tiles[position] == "9"

    def _value_difference(self, position: Vector2D, neighbor: Vector2D) -> int:
        return ord(self._grid.tiles[neighbor]) - ord(self._grid.tiles[position])

    def _neighbors(self, position: Vector2D) -> Iterator[Vector2D]:
        for neighbor in position.adjacent_positions():
            if (
                self._grid.contains(neighbor)
                and self._value_difference(position, neighbor) == 1
            ):
                yield neighbor

    def _hiking_trails_from(self, start: Vector2D) -> Iterator[HikingTrail]:
        visit_stack = [start]
        while visit_stack:
            current_node = visit_stack.pop()
            if self._is_destination(current_node):
                yield HikingTrail(start, current_node)
            else:
                for neighbor in self._neighbors(current_node):
                    visit_stack.append(neighbor)

    def hiking_trails(self) -> Iterator[HikingTrail]:
        for start in self._grid.positions_with_value("0"):
            yield from self._hiking_trails_from(start)
