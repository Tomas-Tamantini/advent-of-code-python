from dataclasses import dataclass
from typing import Iterator

from models.common.vectors import Vector2D

from .reindeer_racer import ReindeerRacer


@dataclass(frozen=True)
class PathState:
    racer: ReindeerRacer
    accumulated_cost: int = 0

    def cost_lower_bound(
        self, end_tile: Vector2D, move_forward_cost: int, turn_cost: int
    ) -> int:
        delta = end_tile - self.racer.position
        lb = self.accumulated_cost + move_forward_cost * delta.manhattan_size
        if delta.x == 0 or delta.y == 0:
            return lb
        else:
            return lb + turn_cost

    @staticmethod
    def _positions_between(start: Vector2D, end: Vector2D) -> Iterator[Vector2D]:
        diff = end - start
        diff_size = diff.manhattan_size
        if diff_size == 0:
            yield start
        else:
            diff_normal = Vector2D(diff.x // diff_size, diff.y // diff_size)
            for i in range(diff_size + 1):
                yield start + i * diff_normal

    def positions_between(self, other: "PathState") -> Iterator[Vector2D]:
        return self._positions_between(self.racer.position, other.racer.position)
