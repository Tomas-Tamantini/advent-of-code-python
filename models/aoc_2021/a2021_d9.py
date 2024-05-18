from models.common.vectors import Vector2D
from typing import Iterator


class SmokeBasin:
    def __init__(self, heightmap: dict[Vector2D, int]):
        self._heightmap = heightmap

    def _neighbors(self, position: Vector2D) -> Iterator[Vector2D]:
        for neighbor in position.adjacent_positions(include_diagonals=False):
            if neighbor in self._heightmap:
                yield neighbor

    def _is_local_minimum(self, position: Vector2D) -> bool:
        return all(
            self._heightmap[position] < self._heightmap[neighbor]
            for neighbor in self._neighbors(position)
        )

    def local_minima(self) -> Iterator[tuple[Vector2D, int]]:
        for position, height in self._heightmap.items():
            if self._is_local_minimum(position):
                yield position, height

    def _flood(self, position: Vector2D) -> set[Vector2D]:
        stack = [position]
        flooded = set()
        while stack:
            current = stack.pop()
            flooded.add(current)
            for neighbor in self._neighbors(current):
                if neighbor not in flooded and self._heightmap[neighbor] != 9:
                    stack.append(neighbor)
        return flooded

    def areas(self) -> Iterator[set[Vector2D]]:
        visited = set()
        for position, height in self._heightmap.items():
            if position in visited or height == 9:
                continue
            area = self._flood(position)
            visited.update(area)
            yield area
