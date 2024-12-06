from models.common.vectors import Vector2D


class PatrolArea:
    def __init__(self, width: int, height: int, obstacles: set[Vector2D]) -> None:
        self._width = width
        self._height = height
        self._obstacles = obstacles

    def is_obstacle(self, position: Vector2D) -> bool:
        return position in self._obstacles

    def is_out_of_bounds(self, position: Vector2D) -> bool:
        return not (0 <= position.x < self._width and 0 <= position.y < self._height)

    def add_obstacle(self, position: Vector2D) -> "PatrolArea":
        return PatrolArea(
            width=self._width,
            height=self._height,
            obstacles=self._obstacles | {position},
        )
