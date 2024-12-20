from dataclasses import dataclass
from math import inf
from typing import Iterable, Iterator

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
    def top_left(self) -> Vector2D:
        return Vector2D(self.min_x, self.max_y)

    @property
    def bottom_right(self) -> Vector2D:
        return Vector2D(self.max_x, self.min_y)

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

    def contains(self, point: Vector2D) -> bool:
        return (
            self.bottom_left.x <= point.x <= self.top_right.x
            and self.bottom_left.y <= point.y <= self.top_right.y
        )

    def all_points_contained(self) -> Iterator[Vector2D]:
        for x in range(self.min_x, self.max_x + 1):
            for y in range(self.min_y, self.max_y + 1):
                yield Vector2D(x, y)

    def intersection(self, other) -> "BoundingBox":
        min_x = max(self.bottom_left.x, other.bottom_left.x)
        max_x = min(self.top_right.x, other.top_right.x)
        min_y = max(self.bottom_left.y, other.bottom_left.y)
        max_y = min(self.top_right.y, other.top_right.y)
        if min_x > max_x or min_y > max_y:
            return None
        return BoundingBox(Vector2D(min_x, min_y), Vector2D(max_x, max_y))

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
