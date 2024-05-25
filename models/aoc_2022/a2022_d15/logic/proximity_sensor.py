from typing import Optional
from dataclasses import dataclass
from models.common.vectors import Vector2D
from models.common.number_theory import Interval


@dataclass(frozen=True)
class ProximitySensor:
    position: Vector2D
    nearest_beacon: Vector2D

    @property
    def _radius(self) -> int:
        return self.position.manhattan_distance(self.nearest_beacon)

    def interval_which_cannot_be_unknown_beacon(self, row: int) -> Optional[Interval]:
        dy = abs(self.position.y - row)
        dx = self._radius - dy
        start_x = self.position.x - dx
        end_x = self.position.x + dx
        return Interval(start_x, end_x) if start_x <= end_x else None

    def interval_which_cannot_be_beacon(self, row: int) -> Optional[Interval]:
        interval = self.interval_which_cannot_be_unknown_beacon(row)
        if interval is None:
            return None
        start_x, end_x = interval.min_inclusive, interval.max_inclusive
        if Vector2D(start_x, row) == self.nearest_beacon:
            start_x += 1
        elif Vector2D(end_x, row) == self.nearest_beacon:
            end_x -= 1
        return Interval(start_x, end_x) if start_x <= end_x else None
