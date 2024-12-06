from dataclasses import dataclass
from typing import Optional

from models.common.number_theory import Interval
from models.common.vectors import Vector2D


@dataclass(frozen=True)
class DiagonalLineSegment:
    x_interval: Interval
    slope_upwards: bool
    offset: int

    def intersection(self, other: "DiagonalLineSegment") -> Optional[Vector2D]:
        if self.slope_upwards == other.slope_upwards:
            raise NotImplementedError("Intersection not implemented for parallel lines")
        sum_offset = other.offset + self.offset
        if sum_offset % 2 != 0:
            return None
        y = sum_offset // 2
        x = self.slope_upwards * (other.offset - self.offset) // 2
        if self.x_interval.contains(x) and other.x_interval.contains(x):
            return Vector2D(x, y)
        return None
