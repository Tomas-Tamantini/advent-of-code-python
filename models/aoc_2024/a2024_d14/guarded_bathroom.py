from collections import defaultdict
from typing import Iterator

from models.common.vectors import Particle2D, Vector2D


class GuardedBathroom:
    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height

    def guard_position_after_time(self, guard: Particle2D, time: int) -> Vector2D:
        position = guard.position_at_time(time)
        return Vector2D(
            x=position.x % self._width,
            y=position.y % self._height,
        )

    def num_guards_per_quadrant(
        self, initial_guards: list[Particle2D], time: int
    ) -> Iterator[int]:
        positions = (self.guard_position_after_time(g, time) for g in initial_guards)
        num_guards = defaultdict(int)
        for pos in positions:
            if pos.x == self._width // 2 or pos.y == self._height // 2:
                continue
            quadrant_id = (pos.x >= self._width // 2, pos.y >= self._height // 2)
            num_guards[quadrant_id] += 1

        yield from num_guards.values()

    def render_guards_at_time(self, guards: list[Particle2D], time: int) -> str:
        positions = (self.guard_position_after_time(g, time) for g in guards)
        grid = [["." for _ in range(self._width)] for _ in range(self._height)]
        for pos in positions:
            grid[pos.y][pos.x] = "#"
        return "\n".join("".join(row) for row in grid)
