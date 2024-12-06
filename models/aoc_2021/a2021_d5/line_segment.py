from dataclasses import dataclass
from typing import Iterator

from models.common.vectors import Vector2D


@dataclass(frozen=True)
class LineSegment:
    start: Vector2D
    end: Vector2D

    @property
    def _delta(self) -> Vector2D:
        return self.end - self.start

    @property
    def is_horizontal(self) -> bool:
        return self._delta.y == 0

    @property
    def is_vertical(self) -> bool:
        return self._delta.x == 0

    @property
    def is_diagonal(self) -> bool:
        return not self.is_horizontal and not self.is_vertical

    def all_points(self) -> Iterator[Vector2D]:
        if not self.is_vertical:
            denominator = abs(self._delta.x)
        else:
            denominator = abs(self._delta.y)
        for i in range(denominator + 1):
            x = self.start.x + (i * self._delta.x) // denominator
            y = self.start.y + (i * self._delta.y) // denominator
            yield Vector2D(x, y)
