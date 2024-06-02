from typing import Iterator
from models.common.vectors import Vector2D
from models.common.graphs import GridMaze


class TunnelMazeGraph(GridMaze):

    def __init__(self) -> None:
        super().__init__()
        self._forbidden_nodes = set()

    def neighbors(self, node: Vector2D) -> Iterator[Vector2D]:
        for neighbor in self._adjacencies[node]:
            if neighbor not in self._forbidden_nodes:
                yield neighbor

    def shortest_distance(
        self, origin: Vector2D, destination: Vector2D, forbidden_nodes: set[Vector2D]
    ) -> float:
        self._forbidden_nodes = forbidden_nodes
        return super().shortest_distance(origin, destination)
