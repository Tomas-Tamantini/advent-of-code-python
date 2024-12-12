from dataclasses import dataclass
from typing import Iterator

from models.common.vectors import CardinalDirection, Vector2D


@dataclass(frozen=True)
class _GardenRegionDimensions:
    area: int
    perimeter: int
    num_sides: int


@dataclass(frozen=True)
class _ContourSegment:
    position: Vector2D
    direction: CardinalDirection


@dataclass(frozen=True)
class _Contour:
    segments: list[_ContourSegment]

    def perimeter(self) -> int:
        return len(self.segments)

    def num_sides(self) -> int:
        return sum(
            1
            for i in range(len(self.segments))
            if self.segments[i].direction
            != self.segments[(i + 1) % len(self.segments)].direction
        )


class GardenRegion:
    def __init__(self, positions: set[Vector2D]):
        self._positions = positions

    def _next_contour_direction(self, segment: _ContourSegment) -> CardinalDirection:
        next_pos = segment.position.move(segment.direction)
        offset = {
            CardinalDirection.EAST: Vector2D(0, 0),
            CardinalDirection.SOUTH: Vector2D(-1, 0),
            CardinalDirection.WEST: Vector2D(-1, 1),
            CardinalDirection.NORTH: Vector2D(0, 1),
        }
        if next_pos + offset[segment.direction] not in self._positions:
            return segment.direction.turn_right()
        elif next_pos + offset[segment.direction.turn_left()] in self._positions:
            return segment.direction.turn_left()
        else:
            return segment.direction

    def _next_contour_segment(self, segment: _ContourSegment) -> _ContourSegment:
        next_pos = segment.position.move(segment.direction)
        return _ContourSegment(next_pos, self._next_contour_direction(segment))

    def _countour_segments(
        self, initial_segment: _ContourSegment
    ) -> Iterator[_ContourSegment]:
        yield initial_segment
        current_segment = self._next_contour_segment(initial_segment)
        while current_segment != initial_segment:
            yield current_segment
            current_segment = self._next_contour_segment(current_segment)

    def _contours(self) -> Iterator[_Contour]:
        visited = set()
        for pos in self._positions:
            neighbor_above = pos.move(CardinalDirection.NORTH)
            if neighbor_above not in self._positions and pos not in visited:
                initial_segment = _ContourSegment(pos, CardinalDirection.EAST)
                segments = list(self._countour_segments(initial_segment))
                yield _Contour(segments)
                for segment in segments:
                    if segment.direction == CardinalDirection.EAST:
                        visited.add(segment.position)

    def dimensions(self) -> _GardenRegionDimensions:
        area = len(self._positions)
        contours = list(self._contours())
        perimeter = sum(c.perimeter() for c in contours)
        num_sides = sum(c.num_sides() for c in contours)
        return _GardenRegionDimensions(area, perimeter, num_sides)
