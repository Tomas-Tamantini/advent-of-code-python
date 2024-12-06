from collections import defaultdict
from bisect import bisect_left
from models.common.vectors import Vector2D, CardinalDirection
from .patrol_guard import PatrolGuard


class PatrolArea:
    def __init__(self, width: int, height: int, obstacles: set[Vector2D]) -> None:
        self._width = width
        self._height = height
        self._obstacles = obstacles
        self._obstacles_per_row = defaultdict(list)
        self._obstacles_per_column = defaultdict(list)
        for obstacle in sorted(obstacles):
            self._obstacles_per_row[obstacle.y].append(obstacle.x)
            self._obstacles_per_column[obstacle.x].append(obstacle.y)

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
        if guard.direction.is_horizontal:
            obstacles = self._obstacles_per_row[guard.position.y]
            guard_position = guard.position.x
        else:
            obstacles = self._obstacles_per_column[guard.position.x]
            guard_position = guard.position.y
        index = bisect_left(obstacles, guard_position)
        obstacle_index = (
            index
            if guard.direction in (CardinalDirection.EAST, CardinalDirection.SOUTH)
            else index - 1
        )
        if obstacle_index < 0:
            return -guard_position - 1
        elif obstacle_index >= len(obstacles):
            return (
                guard_position - self._width
                if guard.direction.is_horizontal
                else guard_position - self._height
            )
        else:
            return abs(obstacles[obstacle_index] - guard_position)
