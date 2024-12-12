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
        # TODO: Refactor
        next_pos = segment.position.move(segment.direction)
        if segment.direction == CardinalDirection.EAST:
            if next_pos not in self._positions:
                return CardinalDirection.SOUTH
            elif next_pos.move(CardinalDirection.NORTH) in self._positions:
                return CardinalDirection.NORTH
            else:
                return CardinalDirection.EAST
        elif segment.direction == CardinalDirection.SOUTH:
            if next_pos.move(CardinalDirection.WEST) not in self._positions:
                return CardinalDirection.WEST
            elif next_pos in self._positions:
                return CardinalDirection.EAST
            else:
                return CardinalDirection.SOUTH
        elif segment.direction == CardinalDirection.WEST:
            if (
                next_pos.move(CardinalDirection.WEST).move(CardinalDirection.NORTH)
                not in self._positions
            ):
                return CardinalDirection.NORTH
            elif next_pos.move(CardinalDirection.WEST) in self._positions:
                return CardinalDirection.SOUTH
            else:
                return CardinalDirection.WEST
        elif next_pos.move(CardinalDirection.NORTH) not in self._positions:
            return CardinalDirection.EAST
        elif (
            next_pos.move(CardinalDirection.WEST).move(CardinalDirection.NORTH)
            in self._positions
        ):
            return CardinalDirection.WEST
        else:
            return CardinalDirection.NORTH

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
                segments = []
                initial_segment = _ContourSegment(pos, CardinalDirection.EAST)
                for segment in self._countour_segments(initial_segment):
                    segments.append(segment)
                    if segment.direction == CardinalDirection.EAST:
                        visited.add(segment.position)
                yield _Contour(segments)

    def dimensions(self) -> _GardenRegionDimensions:
        area = len(self._positions)
        contours = list(self._contours())
        perimeter = sum(c.perimeter() for c in contours)
        num_sides = sum(c.num_sides() for c in contours)
        return _GardenRegionDimensions(area, perimeter, num_sides)
