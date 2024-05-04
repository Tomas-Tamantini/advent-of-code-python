from typing import Iterator
from models.vectors import Vector2D
from models.graphs import dijkstra


class UnderwaterCaveMaze:
    def __init__(self, risk_levels: dict[Vector2D, int]) -> None:
        self._risk_levels = risk_levels

    def risk_level_at(self, position: Vector2D) -> int:
        return self._risk_levels[position]

    def neighbors(self, node: Vector2D) -> Iterator[Vector2D]:
        for neighbor in node.adjacent_positions(include_diagonals=False):
            if neighbor in self._risk_levels:
                yield neighbor

    def weight(self, node_a: Vector2D, node_b: Vector2D) -> float:
        return self._risk_levels[node_b]

    def risk_of_optimal_path(self, start: Vector2D, end: Vector2D) -> int:
        _, cost = dijkstra(start, end, self)
        return cost
