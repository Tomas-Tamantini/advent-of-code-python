from typing import Iterable
from dataclasses import dataclass
from math import inf
from .vector_2d import Vector2D


@dataclass(frozen=True)
class BoundingBox:
    bottom_left: Vector2D
    top_right: Vector2D

    def __post_init__(self) -> None:
        if (
            self.bottom_left.x > self.top_right.x
            or self.bottom_left.y > self.top_right.y
        ):
            raise ValueError("Invalid bounding box coordinates")

    @property
    def min_x(self) -> int:
        return self.bottom_left.x

    @property
    def max_x(self) -> int:
        return self.top_right.x

    @property
    def min_y(self) -> int:
        return self.bottom_left.y

    @property
    def max_y(self) -> int:
        return self.top_right.y

    @property
    def width(self) -> int:
        return self.top_right.x - self.bottom_left.x

    @property
    def height(self) -> int:
        return self.top_right.y - self.bottom_left.y

    @property
    def area(self) -> int:
        return self.width * self.height

    @classmethod
    def from_points(cls, points: Iterable[Vector2D]) -> "BoundingBox":
        if not points:
            return BoundingBox(Vector2D(0, 0), Vector2D(0, 0))
        max_x = max_y = -inf
        min_x = min_y = inf
        for point in points:
            max_x = max(max_x, point.x)
            max_y = max(max_y, point.y)
            min_x = min(min_x, point.x)
            min_y = min(min_y, point.y)
        return BoundingBox(Vector2D(min_x, min_y), Vector2D(max_x, max_y))
