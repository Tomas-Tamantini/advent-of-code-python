from dataclasses import dataclass
from typing import Iterator, Optional

from models.common.number_theory import Interval
from models.common.vectors import Vector2D

from .diagonal_line_segment import DiagonalLineSegment


@dataclass(frozen=True)
class ProximitySensor:
    position: Vector2D
    nearest_beacon: Vector2D

    @property
    def _radius(self) -> int:
        return self.position.manhattan_distance(self.nearest_beacon)

    def is_out_of_reach(self, position: Vector2D) -> bool:
        return self.position.manhattan_distance(position) > self._radius

    def interval_which_cannot_be_beacon(self, row: int) -> Optional[Interval]:
        dy = abs(self.position.y - row)
        dx = self._radius - dy
        start_x = self.position.x - dx
        end_x = self.position.x + dx
        if Vector2D(start_x, row) == self.nearest_beacon:
            start_x += 1
        elif Vector2D(end_x, row) == self.nearest_beacon:
            end_x -= 1
        return Interval(start_x, end_x) if start_x <= end_x else None

    def _left_boundaries(self) -> Iterator[DiagonalLineSegment]:
        x_min = self.position.x - self._radius - 1
        x_max = self.position.x
        x_interval = Interval(x_min, x_max)
        yield DiagonalLineSegment(
            x_interval, slope_upwards=True, offset=self.position.y - x_min
        )
        yield DiagonalLineSegment(
            x_interval, slope_upwards=False, offset=self.position.y + x_min
        )

    def _right_boundaries(self) -> Iterator[DiagonalLineSegment]:
        x_min = self.position.x
        x_max = self.position.x + self._radius + 1
        x_interval = Interval(x_min, x_max)
        yield DiagonalLineSegment(
            x_interval, slope_upwards=True, offset=self.position.y - x_max
        )
        yield DiagonalLineSegment(
            x_interval, slope_upwards=False, offset=self.position.y + x_max
        )

    def boundaries(self) -> Iterator[DiagonalLineSegment]:
        yield from self._left_boundaries()
        yield from self._right_boundaries()
