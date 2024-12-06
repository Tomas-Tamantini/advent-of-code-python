from dataclasses import dataclass
from math import inf
from typing import Iterator

from models.common.vectors import BoundingBox, CardinalDirection, Vector2D


@dataclass(frozen=True)
class WireSegment:
    starting_point: Vector2D
    direction: CardinalDirection
    length: int

    @property
    def ending_point(self) -> Vector2D:
        return self.starting_point.move(self.direction, num_steps=self.length)

    def contains(self, point: Vector2D) -> bool:
        return self._bounding_box.contains(point)

    def distance_to(self, point: Vector2D) -> int:
        return self.starting_point.manhattan_distance(point)

    @property
    def _bounding_box(self) -> BoundingBox:
        return BoundingBox.from_points([self.starting_point, self.ending_point])

    def intersection_points(self, other) -> Iterator[Vector2D]:
        intersection = self._bounding_box.intersection(other._bounding_box)
        if intersection:
            for x in range(intersection.min_x, intersection.max_x + 1):
                for y in range(intersection.min_y, intersection.max_y + 1):
                    yield Vector2D(x, y)


class TwistyWire:
    def __init__(self) -> None:
        self._segments = []

    @property
    def current_end(self) -> Vector2D:
        if not self._segments:
            return Vector2D(0, 0)
        return self._segments[-1].ending_point

    def add_segment(self, direction: CardinalDirection, length: int) -> None:
        segment_start = self.current_end.move(direction)
        self._segments.append(WireSegment(segment_start, direction, length - 1))

    def intersection_points(self, other) -> Iterator[Vector2D]:
        for segment_a in self._segments:
            for segment_b in other._segments:
                yield from segment_a.intersection_points(segment_b)

    def distance_to(self, point: Vector2D) -> int:
        distance = 0
        for segment in self._segments:
            if segment.contains(point):
                return distance + segment.distance_to(point) + 1
            distance += segment.length + 1
        return inf
