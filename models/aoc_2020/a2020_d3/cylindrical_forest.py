from typing import Iterator

from models.common.vectors import Vector2D


class CylindricalForest:
    def __init__(self, width: int, height: int, trees: set[Vector2D]) -> None:
        self._width = width
        self._height = height
        self._trees = trees

    def is_tree_at(self, position: Vector2D) -> bool:
        if position.y >= self._height or position.y < 0:
            raise IndexError(f"y value {position.y} out of bounds")
        actual_x = position.x % self._width
        return Vector2D(actual_x, position.y) in self._trees

    def _positions_along_journey(
        self, steps_right: int, steps_down: int, starting_point: Vector2D
    ) -> Iterator[Vector2D]:
        current_pos = starting_point
        while current_pos.y < self._height:
            yield current_pos
            current_pos += Vector2D(steps_right, steps_down)

    def number_of_collisions_with_trees(
        self,
        steps_right: int,
        steps_down: int,
        starting_point: Vector2D = Vector2D(0, 0),
    ) -> int:
        return sum(
            self.is_tree_at(pos)
            for pos in self._positions_along_journey(
                steps_right, steps_down, starting_point
            )
        )
