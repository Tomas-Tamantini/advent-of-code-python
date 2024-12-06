from models.common.vectors import Vector2D
from .patrol_guard import PatrolGuard


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

    def distance_to_next_obstacle(self, guard: PatrolGuard) -> int:
        # TODO: Optimize
        distance = 0
        while not self.is_obstacle(guard.position):
            guard = guard.move_forward()
            distance += 1
            if self.is_out_of_bounds(guard.position):
                return -distance
        return distance
