from typing import Iterator, Optional

from models.common.graphs import dijkstra
from models.common.vectors import BoundingBox, Vector2D


class UnderwaterCaveMaze:
    def __init__(self, risk_levels: dict[Vector2D, int], extension_factor: int) -> None:
        self._risk_levels = risk_levels
        self._extension_factor = extension_factor
        bounding_box = BoundingBox.from_points(risk_levels.keys())
        self._width = bounding_box.width + 1
        self._height = bounding_box.height + 1

    def _is_valid_position(self, position: Vector2D) -> bool:
        if position.x < 0 or position.y < 0:
            return False
        x_div = position.x // self._width
        y_div = position.y // self._height
        if x_div >= self._extension_factor or y_div >= self._extension_factor:
            return False
        return True

    def risk_level_at(self, position: Vector2D) -> Optional[int]:
        x_div, x_mod = divmod(position.x, self._width)
        y_div, y_mod = divmod(position.y, self._height)
        risk_level = self._risk_levels[Vector2D(x_mod, y_mod)]
        risk_level += x_div + y_div
        while risk_level > 9:
            risk_level -= 9
        return risk_level

    def neighbors(self, node: Vector2D) -> Iterator[Vector2D]:
        for neighbor in node.adjacent_positions(include_diagonals=False):
            if self._is_valid_position(neighbor):
                yield neighbor

    def weight(self, node_a: Vector2D, node_b: Vector2D) -> float:
        return self.risk_level_at(node_b)

    def risk_of_optimal_path(self, start: Vector2D, end: Vector2D) -> int:
        _, cost = dijkstra(start, end, self)
        return cost
