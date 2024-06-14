from typing import Iterator
from models.common.number_theory import Interval
from models.common.vectors import Vector2D, CardinalDirection
from .board_navigator import BoardNavigator


class ObstacleBoard:
    def __init__(self, rows: tuple[Interval], wall_positions: set[Vector2D]) -> None:
        self._rows = rows
        self._cols = tuple(self._build_columns())
        self._wall_positions = wall_positions

    def _build_columns(self) -> Iterator[Interval]:
        max_col_idx = max(row.max_inclusive for row in self._rows)
        for y in range(max_col_idx + 1):
            yield self._build_column(y)

    def _build_column(self, column_idx: int) -> Interval:
        start, end = None, None
        for row_idx, row in enumerate(self._rows):
            if row.contains(column_idx):
                if start is None:
                    start = row_idx
                end = row_idx
            elif start is not None:
                return Interval(start, end)
        return Interval(start, end)

    @property
    def initial_position(self) -> Vector2D:
        return Vector2D(self._rows[0].min_inclusive, 0)

    def _wrap_around(self, position: Vector2D, is_horizontal: bool) -> Vector2D:
        if is_horizontal:
            row = self._rows[position.y]
            if position.x > row.max_inclusive:
                return Vector2D(row.min_inclusive, position.y)
            elif position.x < row.min_inclusive:
                return Vector2D(row.max_inclusive, position.y)
        else:
            col = self._cols[position.x]
            if position.y > col.max_inclusive:
                return Vector2D(position.x, col.min_inclusive)
            elif position.y < col.min_inclusive:
                return Vector2D(position.x, col.max_inclusive)
        return position

    def _next_adjacent_position(
        self, position: Vector2D, facing: CardinalDirection
    ) -> Vector2D:
        new_position = position.move(facing, y_grows_down=True)
        return self._wrap_around(new_position, facing.is_horizontal)

    def next_position(self, navigator: BoardNavigator, num_steps: int) -> Vector2D:
        current_position = navigator.position
        for _ in range(num_steps):
            new_position = self._next_adjacent_position(
                current_position, navigator.facing
            )
            if new_position in self._wall_positions:
                break
            else:
                current_position = new_position
        return current_position
