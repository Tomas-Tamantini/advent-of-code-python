from typing import Iterator
from dataclasses import dataclass
from models.common.vectors import Vector2D, CardinalDirection


@dataclass
class SeaCucumbersHerds:
    east_facing: set[Vector2D]
    south_facing: set[Vector2D]

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, SeaCucumbersHerds):
            return False
        return (
            self.east_facing == value.east_facing
            and self.south_facing == value.south_facing
        )


class SeaCucumbers:
    def __init__(self, width: int, height: int) -> None:
        self._width = width
        self._height = height
        self._some_moved = False

    def _move(
        self, original_position: Vector2D, direction: CardinalDirection
    ) -> Vector2D:
        next_pos = original_position.move(direction, y_grows_down=True)
        if next_pos.x == self._width:
            next_pos = Vector2D(0, next_pos.y)
        elif next_pos.y == self._height:
            next_pos = Vector2D(next_pos.x, 0)
        return next_pos

    def _next_positions(
        self,
        original_positions: set[Vector2D],
        direction: CardinalDirection,
        occupied_positions: set[Vector2D],
    ) -> Iterator[Vector2D]:
        for pos in original_positions:
            next_pos = self._move(pos, direction)
            if next_pos in occupied_positions:
                yield pos
            else:
                self._some_moved = True
                yield next_pos

    def next_state(self, herds: SeaCucumbersHerds) -> SeaCucumbersHerds:
        next_east_facing = set(
            self._next_positions(
                original_positions=herds.east_facing,
                direction=CardinalDirection.EAST,
                occupied_positions=herds.south_facing.union(herds.east_facing),
            )
        )
        next_south_facing = set(
            self._next_positions(
                original_positions=herds.south_facing,
                direction=CardinalDirection.SOUTH,
                occupied_positions=herds.south_facing.union(next_east_facing),
            )
        )
        return SeaCucumbersHerds(
            east_facing=next_east_facing, south_facing=next_south_facing
        )

    def num_steps_until_halt(self, initial_herds: SeaCucumbersHerds) -> int:
        num_steps = 0
        current_herds = initial_herds
        while True:
            num_steps += 1
            self._some_moved = False
            next_herds = self.next_state(current_herds)
            if not self._some_moved:
                break
            current_herds = next_herds
        return num_steps
