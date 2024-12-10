from typing import Iterator

from models.common.io import CharacterGrid
from models.common.vectors import Vector2D

from .trail import HikingTrail


class TopographicMap:
    def __init__(self, grid: CharacterGrid):
        self._grid = grid

    def _is_destination(self, position: Vector2D) -> bool:
        return self._grid.tiles[position] == "9"

    def _neighbors(self, position: Vector2D) -> Iterator[Vector2D]:
        current_value = ord(self._grid.tiles[position])
        for neighbor in position.adjacent_positions():
            if self._grid.contains(neighbor):
                neighbor_value = self._grid.tiles[neighbor]
                if ord(neighbor_value) - current_value == 1:
                    yield neighbor

    def _hiking_trails_from(self, start: Vector2D) -> Iterator[HikingTrail]:
        visited = set()
        visit_stack = [start]
        while visit_stack:
            current_node = visit_stack.pop()
            if current_node in visited:
                continue
            visited.add(current_node)
            if self._is_destination(current_node):
                yield HikingTrail(start, current_node)
            else:
                for neighbor in self._neighbors(current_node):
                    visit_stack.append(neighbor)

    def hiking_trails(self) -> Iterator[HikingTrail]:
        for start in self._grid.positions_with_value("0"):
            yield from self._hiking_trails_from(start)
