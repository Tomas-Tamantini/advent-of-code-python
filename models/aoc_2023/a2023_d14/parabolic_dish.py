from typing import Iterator
from models.common.vectors import Vector2D, CardinalDirection
from dataclasses import dataclass


@dataclass(frozen=True)
class _TiltedSlice:
    slice_index: int
    slice_size: int
    tilt_direction: CardinalDirection

    def initial_obstacle(self) -> Vector2D:
        if self.tilt_direction == CardinalDirection.NORTH:
            return Vector2D(self.slice_index, -1)
        elif self.tilt_direction == CardinalDirection.SOUTH:
            return Vector2D(self.slice_index, self.slice_size)
        elif self.tilt_direction == CardinalDirection.WEST:
            return Vector2D(-1, self.slice_index)
        else:
            return Vector2D(self.slice_size, self.slice_index)

    def positions(self) -> Iterator[Vector2D]:
        if self.tilt_direction == CardinalDirection.NORTH:
            for row_idx in range(self.slice_size):
                yield Vector2D(self.slice_index, row_idx)
        elif self.tilt_direction == CardinalDirection.SOUTH:
            for row_idx in reversed(range(self.slice_size)):
                yield Vector2D(self.slice_index, row_idx)
        elif self.tilt_direction == CardinalDirection.WEST:
            for column_idx in range(self.slice_size):
                yield Vector2D(column_idx, self.slice_index)
        else:
            for column_idx in reversed(range(self.slice_size)):
                yield Vector2D(column_idx, self.slice_index)


class ParabolicDish:
    def __init__(self, width: int, height: int, cube_rocks: set[Vector2D]) -> None:
        self._width = width
        self._height = height
        self._cube_rocks = cube_rocks

    def _tilt_slice(
        self,
        slice: _TiltedSlice,
        rounded_rocks: set[Vector2D],
    ) -> Iterator[Vector2D]:
        current_obstacle_pos = slice.initial_obstacle()
        for pos in slice.positions():
            if pos in self._cube_rocks:
                current_obstacle_pos = pos
            elif pos in rounded_rocks:
                current_obstacle_pos = current_obstacle_pos.move(
                    slice.tilt_direction.reverse(), y_grows_down=True
                )
                yield current_obstacle_pos

    def tilt(
        self, rounded_rocks: set[Vector2D], direction: CardinalDirection
    ) -> Iterator[Vector2D]:
        num_slices, slice_size = (
            (self._width, self._height)
            if direction.is_vertical
            else (self._height, self._width)
        )
        for slice_idx in range(num_slices):
            slice = _TiltedSlice(slice_idx, slice_size, direction)
            yield from self._tilt_slice(slice, rounded_rocks)

    def load_from_south_edge(self, rounded_rocks: set[Vector2D]) -> int:
        return sum(self._height - pos.y for pos in rounded_rocks)
