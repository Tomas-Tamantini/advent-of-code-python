from models.vectors import Vector2D
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
