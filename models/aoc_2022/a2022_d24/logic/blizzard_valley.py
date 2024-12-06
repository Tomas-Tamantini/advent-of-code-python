from collections import defaultdict
from dataclasses import dataclass

from models.common.vectors import CardinalDirection, Vector2D

from .blizzard import Blizzard


@dataclass(frozen=True)
class _HorizontalBlizzard:
    row: int
    initial_column: int
    increment: int

    def position_at_time(self, time: int, valley_width) -> Vector2D:
        x = (self.initial_column + time * self.increment - 1) % (valley_width - 2) + 1
        return Vector2D(x, self.row)


@dataclass(frozen=True)
class _VerticalBlizzard:
    column: int
    initial_row: int
    increment: int

    def position_at_time(self, time: int, valley_height) -> Vector2D:
        y = (self.initial_row + time * self.increment - 1) % (valley_height - 2) + 1
        return Vector2D(self.column, y)


class BlizzardValley:
    def __init__(
        self,
        height: int,
        width: int,
        entrance: Vector2D,
        exit: Vector2D,
        blizzards: set[Blizzard],
    ):
        self._height = height
        self._width = width
        self._entrance = entrance
        self._exit = exit
        horizontal_blizzards = {
            _HorizontalBlizzard(
                row=blizzard.initial_position.y,
                initial_column=blizzard.initial_position.x,
                increment=1 if blizzard.direction == CardinalDirection.EAST else -1,
            )
            for blizzard in blizzards
            if blizzard.direction.is_horizontal
        }
        vertical_blizzards = {
            _VerticalBlizzard(
                column=blizzard.initial_position.x,
                initial_row=blizzard.initial_position.y,
                increment=1 if blizzard.direction == CardinalDirection.SOUTH else -1,
            )
            for blizzard in blizzards
            if blizzard.direction.is_vertical
        }
        self._horizontal_blizzards = defaultdict(set)
        for blizzard in horizontal_blizzards:
            self._horizontal_blizzards[blizzard.row].add(blizzard)

        self._vertical_blizzards = defaultdict(set)
        for blizzard in vertical_blizzards:
            self._vertical_blizzards[blizzard.column].add(blizzard)

    @property
    def entrance(self) -> Vector2D:
        return self._entrance

    @property
    def exit(self) -> Vector2D:
        return self._exit

    def _is_border(self, position: Vector2D) -> bool:
        return (
            position.x <= 0
            or position.x >= self._width - 1
            or position.y <= 0
            or position.y >= self._height - 1
        )

    def is_wall(self, position: Vector2D) -> bool:
        return self._is_border(position) and position not in {
            self._entrance,
            self._exit,
        }

    def _position_is_occupied_by_blizzard(self, position: Vector2D, time: int) -> bool:
        return any(
            blizzard.position_at_time(time, self._width) == position
            for blizzard in self._horizontal_blizzards[position.y]
        ) or any(
            blizzard.position_at_time(time, self._height) == position
            for blizzard in self._vertical_blizzards[position.x]
        )

    def position_is_free_at_time(self, position: Vector2D, time: int) -> bool:
        return not self.is_wall(
            position
        ) and not self._position_is_occupied_by_blizzard(position, time)
