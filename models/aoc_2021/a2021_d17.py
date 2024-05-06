from typing import Iterator, Iterable
from math import floor, ceil, sqrt
from models.vectors import Vector2D, BoundingBox


class UnderwaterProjectile:
    @staticmethod
    def position_at(step: int, initial_velocity: Vector2D) -> Vector2D:
        mx = min(initial_velocity.x + 1, step)
        x = (-mx * mx + mx * (2 * initial_velocity.x + 1)) // 2
        y = (-step * step + step * (2 * initial_velocity.y + 1)) // 2
        return Vector2D(x, y)

    @staticmethod
    def maximum_height(initial_y_velocity: Vector2D) -> int:
        return (initial_y_velocity * (initial_y_velocity + 1)) // 2

    @staticmethod
    def _trajectory_intersects_target(
        target: BoundingBox, initial_velocity: Vector2D, candidate_steps: Iterable[int]
    ) -> bool:
        for step in candidate_steps:
            position = UnderwaterProjectile.position_at(step, initial_velocity)
            if target.contains(position):
                return True
        return False

    @staticmethod
    def _possible_intersection_interval(
        initial_y_velocity: int, target: BoundingBox
    ) -> tuple[int, int]:
        gy = initial_y_velocity + 0.5
        interval_start = gy + sqrt(gy * gy - 2 * target.max_y)
        interval_end = gy + sqrt(gy * gy - 2 * target.min_y)
        return ceil(interval_start), floor(interval_end) + 1

    @staticmethod
    def velocities_to_reach_target(target: BoundingBox) -> Iterator[Vector2D]:
        if target.max_y >= 0 or target.min_x <= 0:
            raise NotImplementedError(
                "Target must be below origin and to the right of it"
            )

        for vy in range(target.min_y, 1 - target.min_y):
            interval_start, interval_end = (
                UnderwaterProjectile._possible_intersection_interval(vy, target)
            )
            for vx in range(target.max_x + 1):
                candidate = Vector2D(vx, vy)
                interval = range(interval_start, interval_end)
                if UnderwaterProjectile._trajectory_intersects_target(
                    target, candidate, interval
                ):
                    yield candidate
