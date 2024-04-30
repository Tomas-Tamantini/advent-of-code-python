from dataclasses import dataclass
from typing import Iterator
from models.vectors import Vector2D, BoundingBox


@dataclass(frozen=True)
class LineSegment:
    start: Vector2D
    end: Vector2D

    @property
    def is_horizontal(self) -> bool:
        return self.start.y == self.end.y

    @property
    def is_vertical(self) -> bool:
        return self.start.x == self.end.x

    @property
    def _bounding_box(self) -> BoundingBox:
        return BoundingBox.from_points((self.start, self.end))

    def intersection(self, other: "LineSegment") -> Iterator[Vector2D]:
        box_intersection = self._bounding_box.intersection(other._bounding_box)
        if box_intersection:
            yield from box_intersection.all_points_contained()
