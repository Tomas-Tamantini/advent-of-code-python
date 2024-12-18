from typing import Iterator

from models.common.graphs import a_star
from models.common.vectors import Vector2D


class Memory2D:
    def __init__(self, width: int, height: int, corrupted_positions: list[Vector2D]):
        self._width = width
        self._height = height
        self._corrupted_positions = corrupted_positions
        self._end_position = None

    def _is_within_bounds(self, pos: Vector2D) -> bool:
        return 0 <= pos.x < self._width and 0 <= pos.y < self._height

    def neighbors(self, node: Vector2D) -> Iterator[Vector2D]:
        for pos in node.adjacent_positions():
            if self._is_within_bounds(pos) and (pos not in self._corrupted_positions):
                yield pos

    @staticmethod
    def weight(node_a: Vector2D, node_b: Vector2D) -> int:
        return 1

    def heuristic_potential(self, node: Vector2D) -> int:
        return node.manhattan_distance(self._end_position)

    def shortest_path(self, start: Vector2D, end: Vector2D) -> int:
        self._end_position = end
        return a_star(
            origin=start, is_destination=lambda position: position == end, graph=self
        )[1]
